import requests
import json
from datetime import datetime, timedelta

# Constants
BOE_BASE_URL = 'https://www.boe.es'
API_BASE_URL = 'https://www.boe.es/datosabiertos/api'

def search_boe_oposiciones_alicante():
    """Search for oposiciones in Alicante province from BOE"""
    headers = {'Accept': 'application/json'}

    # Try to get recent BOE issues
    oposiciones = []
    today = datetime.now()

    # Search in the last 7 days
    for days_back in range(7):
        search_date = today - timedelta(days=days_back)
        date_str = search_date.strftime('%Y%m%d')

        try:
            url = f"{API_BASE_URL}/boe/sumario/{date_str}"
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                daily_oposiciones = extract_alicante_oposiciones(data, date_str)
                oposiciones.extend(daily_oposiciones)

        except Exception as e:
            print("Error fetching BOE for {}: {}".format(date_str, str(e)))
            continue

    return oposiciones

def extract_alicante_oposiciones(data, date_str):
    """Extract oposiciones from BOE data that mention Alicante"""
    oposiciones = []

    if not data or 'data' not in data or 'sumario' not in data['data']:
        return oposiciones

    sumario = data['data']['sumario']
    diario_list = sumario.get('diario', [])

    for diario_item in diario_list:
        secciones = diario_item.get('seccion', [])

        for seccion in secciones:
            # Look for oposiciones section
            if 'oposiciones' in seccion.get('nombre', '').lower():
                departamentos = seccion.get('departamento', [])
                if not isinstance(departamentos, list):
                    departamentos = [departamentos]

                for departamento in departamentos:
                    # Look for "Personal funcionario y laboral" section
                    texto = departamento.get('texto', {})
                    if isinstance(texto, dict):
                        epigrafes = texto.get('epigrafe', [])
                        if not isinstance(epigrafes, list):
                            epigrafes = [epigrafes]

                        for epigrafe in epigrafes:
                            if epigrafe.get('nombre') == "Personal funcionario y laboral":
                                items = epigrafe.get('item', [])
                                if not isinstance(items, list):
                                    items = [items]

                                for item in items:
                                    if isinstance(item, dict):
                                        titulo = item.get('titulo', '').lower()

                                        # Filter for Alicante and auxiliar administrativo
                                        if ('alicante' in titulo or 'alacant' in titulo) and \
                                           ('auxiliar administrativo' in titulo or 'auxiliar' in titulo):

                                            oposicion = {
                                                'titulo': item.get('titulo'),
                                                'fecha_publicacion': date_str,
                                                'identificador': item.get('identificador'),
                                                'url_html': item.get('url_html'),
                                                'url_pdf': item.get('url_pdf', {}).get('texto') if isinstance(item.get('url_pdf'), dict) else item.get('url_pdf'),
                                                'plazo_abierto': check_plazo_abierto(item)
                                            }
                                            oposiciones.append(oposicion)

    return oposiciones

def check_plazo_abierto(item):
    """Check if the application deadline is still open"""
    # This is a simplified check - in reality, you'd need to parse the actual content
    # For now, we'll assume recent publications (last 30 days) have open deadlines
    try:
        fecha_pub = item.get('fecha_publicacion') or item.get('fecha_disponible')
        if fecha_pub:
            pub_date = datetime.strptime(fecha_pub, '%Y%m%d')
            days_since = (datetime.now() - pub_date).days
            # Assume deadlines are open for 30 days after publication
            return days_since <= 30
    except:
        pass
    return False

def get_oposiciones_data():
    """Main function to get oposiciones data"""
    try:
        oposiciones = search_boe_oposiciones_alicante()
        # Filter only those with open deadlines
        open_oposiciones = [opp for opp in oposiciones if opp['plazo_abierto']]
        return {'oposiciones': open_oposiciones, 'total': len(open_oposiciones)}
    except Exception as e:
        print("Error getting oposiciones data: {}".format(str(e)))
        return {'oposiciones': [], 'total': 0}