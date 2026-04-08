import requests
import json
from datetime import datetime, timedelta
import re
from bs4 import BeautifulSoup

# Constants
BOE_BASE_URL = 'https://www.boe.es'
API_BASE_URL = 'https://www.boe.es/datosabiertos/api'
DOGV_BASE_URL = 'https://dogv.gva.es'
DIPUTACION_ALICANTE_URL = 'https://www.dip-alicante.es'

def search_all_public_jobs_alicante():
    """Search for all public job offers in Alicante from multiple sources"""
    all_jobs = []

    # 1. BOE (Estado Español)
    boe_jobs = search_boe_jobs()
    all_jobs.extend(boe_jobs)

    # 2. DOGV (Generalitat Valenciana)
    dogv_jobs = search_dogv_jobs()
    all_jobs.extend(dogv_jobs)

    # 3. Diputación de Alicante
    diputacion_jobs = search_diputacion_jobs()
    all_jobs.extend(diputacion_jobs)

    # 4. Ayuntamientos de Alicante
    ayuntamientos_jobs = search_ayuntamientos_jobs()
    all_jobs.extend(ayuntamientos_jobs)

    # 5. Unión Europea (EUR-Lex)
    ue_jobs = search_ue_jobs()
    all_jobs.extend(ue_jobs)

    return all_jobs

def search_boe_jobs():
    """Search for jobs in BOE"""
    headers = {'Accept': 'application/json'}
    jobs = []
    today = datetime.now()

    for days_back in range(7):
        search_date = today - timedelta(days=days_back)
        date_str = search_date.strftime('%Y%m%d')

        try:
            url = f"{API_BASE_URL}/boe/sumario/{date_str}"
            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                data = response.json()
                daily_jobs = extract_jobs_from_boe(data, date_str, 'BOE - Estado Español')
                jobs.extend(daily_jobs)

        except Exception as e:
            print("Error fetching BOE for {}: {}".format(date_str, str(e)))
            continue

    return jobs

def search_dogv_jobs():
    """Search for jobs in DOGV (Diario Oficial de la Generalitat Valenciana)"""
    jobs = []
    try:
        # DOGV API - intentar acceder a través de web scraping básico
        today = datetime.now()
        date_str = today.strftime('%Y%m%d')

        # Intentar acceder a la API del DOGV si existe
        url = f"{DOGV_BASE_URL}/api/v1/diario"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            data = response.json()
            # Procesar datos del DOGV
            dogv_jobs = extract_jobs_from_dogv(data, date_str, 'DOGV - Generalitat Valenciana')
            jobs.extend(dogv_jobs)
        else:
            # Fallback: crear entrada simulada para desarrollo
            jobs.append({
                'titulo': 'Sistema DOGV en desarrollo',
                'fecha_publicacion': date_str,
                'fuente': 'DOGV - Generalitat Valenciana',
                'tipo': 'Desarrollo',
                'url_html': f"{DOGV_BASE_URL}",
                'plazo_abierto': True,
                'categoria': 'Sistema'
            })

    except Exception as e:
        print("Error fetching DOGV: {}".format(str(e)))
        # Fallback entry
        jobs.append({
            'titulo': 'DOGV temporalmente no disponible',
            'fecha_publicacion': datetime.now().strftime('%Y%m%d'),
            'fuente': 'DOGV - Generalitat Valenciana',
            'tipo': 'Temporal',
            'url_html': f"{DOGV_BASE_URL}",
            'plazo_abierto': True,
            'categoria': 'Sistema'
        })

    return jobs

def search_diputacion_jobs():
    """Search for jobs in Diputación de Alicante"""
    jobs = []
    try:
        # Intentar acceder al portal de empleo de la Diputación
        url = f"{DIPUTACION_ALICANTE_URL}/empleo"
        response = requests.get(url, timeout=10)

        if response.status_code == 200:
            # Extraer ofertas de empleo del HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            job_listings = soup.find_all(['div', 'article'], class_=re.compile(r'job|empleo|oferta'))

            for job in job_listings[:5]:  # Limitar a 5 ofertas
                title = job.find(['h3', 'h4', 'a'])
                if title:
                    link_elem = job.find('a')
                    url = f"{DIPUTACION_ALICANTE_URL}"
                    if link_elem and link_elem.get('href'):
                        url = f"{DIPUTACION_ALICANTE_URL}{link_elem['href']}"

                    jobs.append({
                        'titulo': title.get_text().strip(),
                        'fecha_publicacion': datetime.now().strftime('%Y%m%d'),
                        'fuente': 'Diputación de Alicante',
                        'tipo': 'Empleo Público',
                        'url_html': url,
                        'plazo_abierto': True,
                        'categoria': 'Administración Local'
                    })
        else:
            # Fallback
            jobs.append({
                'titulo': 'Portal de empleo Diputación Alicante',
                'fecha_publicacion': datetime.now().strftime('%Y%m%d'),
                'fuente': 'Diputación de Alicante',
                'tipo': 'Portal',
                'url_html': f"{DIPUTACION_ALICANTE_URL}/empleo",
                'plazo_abierto': True,
                'categoria': 'Administración Local'
            })

    except Exception as e:
        print("Error fetching Diputación: {}".format(str(e)))
        jobs.append({
            'titulo': 'Diputación Alicante - Portal de empleo',
            'fecha_publicacion': datetime.now().strftime('%Y%m%d'),
            'fuente': 'Diputación de Alicante',
            'tipo': 'Portal',
            'url_html': f"{DIPUTACION_ALICANTE_URL}/empleo",
            'plazo_abierto': True,
            'categoria': 'Administración Local'
        })

    return jobs

def search_ayuntamientos_jobs():
    """Search for jobs in Alicante municipalities"""
    jobs = []

    # Lista de principales ayuntamientos de Alicante
    ayuntamientos = [
        ('Alicante/Alacant', 'https://www.alicante.es'),
        ('Elche/Elx', 'https://www.elche.es'),
        ('Torrevieja', 'https://www.torrevieja.es'),
        ('Orihuela', 'https://www.orihuela.es'),
        ('Benidorm', 'https://www.benidorm.org'),
        ('Alcoy/Alcoi', 'https://www.alcoi.org'),
        ('Villena', 'https://www.villena.es'),
        ('Elda', 'https://www.elda.es'),
        ('San Vicente del Raspeig', 'https://www.sanvicente.es'),
        ('Aspe', 'https://www.aspe.es')
    ]

    for nombre, url_base in ayuntamientos:
        try:
            # Intentar acceder a secciones de empleo/rrhh
            urls_to_try = [
                f"{url_base}/empleo",
                f"{url_base}/rrhh",
                f"{url_base}/personal",
                f"{url_base}/ofertas-empleo",
                url_base
            ]

            for url in urls_to_try:
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        jobs.append({
                            'titulo': f'Portal de empleo - Ayuntamiento de {nombre}',
                            'fecha_publicacion': datetime.now().strftime('%Y%m%d'),
                            'fuente': f'Ayuntamiento de {nombre}',
                            'tipo': 'Empleo Municipal',
                            'url_html': url,
                            'plazo_abierto': True,
                            'categoria': 'Administración Local'
                        })
                        break  # Usar primera URL que funcione
                except:
                    continue

        except Exception as e:
            print("Error fetching {}: {}".format(nombre, str(e)))
            jobs.append({
                'titulo': f'Ayuntamiento de {nombre} - Web municipal',
                'fecha_publicacion': datetime.now().strftime('%Y%m%d'),
                'fuente': f'Ayuntamiento de {nombre}',
                'tipo': 'Web Municipal',
                'url_html': url_base,
                'plazo_abierto': True,
                'categoria': 'Administración Local'
            })

    return jobs

def search_ue_jobs():
    """Search for EU jobs related to Spain/Alicante"""
    jobs = []
    try:
        # EUR-Lex API para empleos públicos europeos
        url = "https://eur-lex.europa.eu/search.html"
        params = {
            'type': 'quick',
            'scope': 'EURLEX',
            'text': 'empleo público España Alicante',
            'lang': 'es'
        }

        response = requests.get(url, params=params, timeout=10)

        if response.status_code == 200:
            jobs.append({
                'titulo': 'Portal de empleo europeo - EUR-Lex',
                'fecha_publicacion': datetime.now().strftime('%Y%m%d'),
                'fuente': 'Unión Europea - EUR-Lex',
                'tipo': 'Empleo Europeo',
                'url_html': url,
                'plazo_abierto': True,
                'categoria': 'Administración Europea'
            })

        # Añadir EPSO (European Personnel Selection Office)
        jobs.append({
            'titulo': 'EPSO - Concursos de la Unión Europea',
            'fecha_publicacion': datetime.now().strftime('%Y%m%d'),
            'fuente': 'Unión Europea - EPSO',
            'tipo': 'Concursos Europeos',
            'url_html': 'https://epso.europa.eu/es',
            'plazo_abierto': True,
            'categoria': 'Administración Europea'
        })

    except Exception as e:
        print("Error fetching UE jobs: {}".format(str(e)))
        jobs.append({
            'titulo': 'EPSO - Concursos Unión Europea',
            'fecha_publicacion': datetime.now().strftime('%Y%m%d'),
            'fuente': 'Unión Europea - EPSO',
            'tipo': 'Concursos Europeos',
            'url_html': 'https://epso.europa.eu/es',
            'plazo_abierto': True,
            'categoria': 'Administración Europea'
        })

    return jobs

def extract_jobs_from_boe(data, date_str, fuente):
    """Extract jobs from BOE data"""
    jobs = []

    if not data or 'data' not in data or 'sumario' not in data['data']:
        return jobs

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

                                        # Filter for Alicante and public jobs (administration and communication)
                                        alicante_found = ('alicante' in titulo or 'alacant' in titulo)
                                        admin_communication_found = (
                                            'auxiliar' in titulo or 'administrativo' in titulo or
                                            'funcionario' in titulo or 'oposicion' in titulo or
                                            'tecnico superior comunicacion' in titulo or 'tecnico comunicacion' in titulo or
                                            'periodista' in titulo or 'redactor gabinete prensa' in titulo or 'redactor prensa' in titulo or
                                            'coordinador comunicacion' in titulo or 'coordinadora comunicacion' in titulo or
                                            'community manager' in titulo or 'responsable redes sociales' in titulo or
                                            'analista medios' in titulo or 'analista comunicacion' in titulo or
                                            'asesor prensa' in titulo or 'asesor comunicacion' in titulo or
                                            'gestion crisis' in titulo or 'produccion contenidos' in titulo or
                                            'relaciones informativas' in titulo or 'comunicacion institucional' in titulo
                                        )

                                        if alicante_found and admin_communication_found:

                                             # Determinar categoría basada en el contenido
                                             categoria = 'Administración del Estado'
                                             if any(term in titulo for term in [
                                                 'comunicacion', 'periodista', 'redactor', 'coordinador comunicacion',
                                                 'community manager', 'redes sociales', 'analista medios',
                                                 'asesor prensa', 'gestion crisis', 'produccion contenidos',
                                                 'relaciones informativas', 'comunicacion institucional'
                                             ]):
                                                 categoria = 'Comunicación'

                                             job = {
                                                 'titulo': item.get('titulo'),
                                                 'fecha_publicacion': date_str,
                                                 'fuente': fuente,
                                                 'tipo': 'Oposición/Concurso',
                                                 'url_html': item.get('url_html'),
                                                 'url_pdf': item.get('url_pdf', {}).get('texto') if isinstance(item.get('url_pdf'), dict) else item.get('url_pdf'),
                                                 'plazo_abierto': check_plazo_abierto(item),
                                                 'categoria': categoria,
                                                 'identificador': item.get('identificador')
                                             }
                                             jobs.append(job)

    return jobs

def extract_jobs_from_dogv(data, date_str, fuente):
    """Extract jobs from DOGV data"""
    jobs = []
    # Implementar extracción específica del DOGV cuando esté disponible
    return jobs

def check_plazo_abierto(item):
    """Check if the application deadline is still open"""
    try:
        fecha_pub = item.get('fecha_publicacion') or item.get('fecha_disponible')
        if fecha_pub:
            pub_date = datetime.strptime(fecha_pub, '%Y%m%d')
            days_since = (datetime.now() - pub_date).days
            # Assume deadlines are open for 30 days after publication
            return days_since <= 30
    except:
        pass
    return True  # Default to open for non-BOE sources

def get_all_jobs_data():
    """Main function to get all job offers data"""
    try:
        jobs = search_all_public_jobs_alicante()
        # Filter only those with open deadlines
        open_jobs = [job for job in jobs if job['plazo_abierto']]
        return {'jobs': open_jobs, 'total': len(open_jobs)}
    except Exception as e:
        print("Error getting jobs data: {}".format(str(e)))
        return {'jobs': [], 'total': 0}