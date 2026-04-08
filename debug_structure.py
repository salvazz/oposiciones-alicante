import requests
import json
from datetime import datetime

BASE_BOE_API_URL = 'https://www.boe.es/datosabiertos/api'

def debug_structure():
    headers = {'Accept': 'application/json'}
    today = datetime.now().strftime('%Y%m%d')
    url = f"{BASE_BOE_API_URL}/boe/sumario/{today}"
    
    print(f"Fetching from: {url}")
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print("Full response structure:")
        print(json.dumps(data, indent=2))
        
        # Extract and show some sample items that might be oposiciones
        if 'data' in data and 'sumario' in data['data']:
            sumario = data['data']['sumario']
            diario_list = sumario.get('diario', [])
            
            print(f"\nFound {len(diario_list)} diario items")
            
            # Look through all diario items for oposiciones
            oposiciones_found = []
            for diario_idx, diario_item in enumerate(diario_list):
                secciones = diario_item.get('seccion', [])
                for seccion_idx, seccion in enumerate(secciones):
                    departamento = seccion.get('departamento', {})
                    if isinstance(departamento, list):
                        dept_list = departamento
                    else:
                        dept_list = [departamento] if departamento else []
                    
                    for dept in dept_list:
                        texto = dept.get('texto', {})
                        if isinstance(texto, dict) and 'epigrafe' in texto:
                            epigrafes = texto['epigrafe']
                            if isinstance(epigrafes, list):
                                for epigrafe in epigrafes:
                                    if isinstance(epigrafe, dict):
                                        item = epigrafe.get('item', {})
                                        if isinstance(item, dict):
                                            titulo = item.get('titulo', '').lower()
                                            if 'oposicion' in titulo or 'oposición' in titulo or 'convocatoria' in titulo:
                                                oposiciones_found.append({
                                                    'diario_num': diario_item.get('numero'),
                                                    'seccion': seccion.get('nombre'),
                                                    'departamento': dept.get('nombre'),
                                                    'titulo': item.get('titulo'),
                                                    'fecha': item.get('fecha_publicacion') or item.get('fecha_disponible') or sumario.get('metadatos', {}).get('fecha_publicacion'),
                                                    'link_html': item.get('url_html'),
                                                    'link_pdf': item.get('url_pdf', {}).get('texto') if isinstance(item.get('url_pdf'), dict) else item.get('url_pdf')
                                                })
            
            print(f"\nFound {len(oposiciones_found)} oposiciones-related items:")
            for i, opp in enumerate(oposiciones_found[:10]):  # Show first 10
                print(f"{i+1}. {opp['titulo'][:100]}...")
                print(f"   Fecha: {opp['fecha']}")
                print(f"   Link: {opp['link_html']}")
                print()
    else:
        print(f"Error: {response.status_code}")
        print(response.text[:500])

if __name__ == "__main__":
    debug_structure()