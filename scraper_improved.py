import requests
import json
import csv
from datetime import datetime, timedelta

# Constants
BASE_BOE_API_URL = 'https://www.boe.es/datosabiertos/api'
OUTPUT_JSON = 'job_opportunities.json'
OUTPUT_CSV = 'job_opportunities.csv'
OUTPUT_HTML = 'job_opportunities.html'

def fetch_job_opportunities():
    """Fetch job opportunities data from BOE API"""
    headers = {'Accept': 'application/json'}
    today = datetime.now().strftime('%Y%m%d')
    url = f"{BASE_BOE_API_URL}/boe/sumario/{today}"
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get('data'):
                print(f"Successfully fetched data from {url}")
                return data
            else:
                print("No data found in response")
                return None
        else:
            print(f'Error fetching data from BOE API: {response.status_code}')
            return None
    except Exception as e:
        print(f"Error fetching from {url}: {str(e)}")
        return None

def extract_oposiciones_from_sumario(data):
    """Extract oposiciones from BOE sumario data structure"""
    oposiciones = []
    
    if not data or 'data' not in data or 'sumario' not in data['data']:
        return oposiciones
    
    sumario = data['data']['sumario']
    fecha_publicacion = sumario.get('metadatos', {}).get('fecha_publicacion')
    
    # Navigate through the diario structure
    diario_list = sumario.get('diario', [])
    
    for diario_item in diario_list:
        secciones = diario_item.get('seccion', [])
        
        for seccion in secciones:
            # Look for the "Oposiciones y concursos" section
            if seccion.get('nombre') == "II. Autoridades y personal. - B. Oposiciones y concursos":
                departamentos = seccion.get('departamento', [])
                if not isinstance(departamentos, list):
                    departamentos = [departamentos]
                
                for departamento in departamentos:
                    epigrafes = departamento.get('texto', {}).get('epigrafe', [])
                    if not isinstance(epigrafes, list):
                        epigrafes = [epigrafes]
                    
                    for epigrafe in epigrafes:
                        # Look for "Personal funcionario y laboral" which contains oposiciones
                        if epigrafe.get('nombre') == "Personal funcionario y laboral":
                            items = epigrafe.get('item', [])
                            if not isinstance(items, list):
                                items = [items]
                            
                            for item in items:
                                if isinstance(item, dict):
                                    titulo = item.get('titulo', '')
                                    # Filter for Alicante/Alacant mentions
                                    if 'alicante' in titulo.lower() or 'alacant' in titulo.lower():
                                        # Extract date from item or use publication date
                                        fecha = item.get('fecha_publicacion') or \
                                               item.get('fecha_disponible') or \
                                               fecha_publicacion
                                        
                                        # Extract links
                                        link_html = item.get('url_html')
                                        link_pdf = None
                                        url_pdf = item.get('url_pdf')
                                        if isinstance(url_pdf, dict):
                                            link_pdf = url_pdf.get('texto')
                                        else:
                                            link_pdf = url_pdf
                                        
                                        oposiciones.append({
                                            'title': titulo,
                                            'link': link_html or link_pdf or '',
                                            'date': fecha,
                                            'identifier': item.get('identificador'),
                                            'control': item.get('control')
                                        })
    
    return oposiciones

def filter_by_date(opportunities, date):
    """Filter job opportunities by date"""
    filtered_opportunities = []
    for opp in opportunities:
        # Handle different date formats
        date_str = opp.get('date')
        if date_str:
            try:
                # Convert YYYYMMDD to datetime object
                opp_date = datetime.strptime(date_str, '%Y%m%d')
                if opp_date >= date:
                    filtered_opportunities.append(opp)
            except ValueError:
                # If date format is different, try alternative formats
                try:
                    opp_date = datetime.strptime(date_str, '%Y-%m-%d')
                    if opp_date >= date:
                        filtered_opportunities.append(opp)
                except ValueError:
                    # Skip if we can't parse the date
                    continue
    return filtered_opportunities

def save_to_json(data):
    """Save data to JSON file"""
    with open(OUTPUT_JSON, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def save_to_csv(data):
    """Save data to CSV file"""
    with open(OUTPUT_CSV, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title', 'Link', 'Date'])  # Header
        for item in data:
            writer.writerow([item['title'], item['link'], item['date']])

def save_to_html(data):
    """Save data to HTML file"""
    with open(OUTPUT_HTML, 'w') as html_file:
        html_file.write('<html><body><table>')
        html_file.write('<tr><th>Title</th><th>Link</th><th>Date</th></tr>')
        for item in data:
            # Escape HTML special characters in title
            title = item['title'].replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            link = item['link'] or '#'
            date = item['date'] or ''
            html_file.write(f'<tr><td>{title}</td><td><a href="{link}" target="_blank">{link}</a></td><td>{date}</td></tr>')
        html_file.write('</table></body></html>')

def main():
    # Set the date filter (e.g., opportunities from the last 30 days)
    date_filter = datetime.now() - timedelta(days=30)
    
    # Fetch opportunities
    raw_data = fetch_job_opportunities()
    if raw_data:
        # Extract oposiciones from the raw data
        opportunities = extract_oposiciones_from_sumario(raw_data)
        print(f"Found {len(opportunities)} oposiciones related to Alicante/Alacant")
        
        if opportunities:
            # Validate links (optional, can be slow)
            # valid_opportunities = [opp for opp in opportunities if validate_link(opp['link'])]
            valid_opportunities = opportunities  # Skip validation for now
            
            # Filter by date
            filtered_opportunities = filter_by_date(valid_opportunities, date_filter)
            print(f"After date filtering: {len(filtered_opportunities)} opportunities")
            
            # Save the results
            save_to_json(filtered_opportunities)
            save_to_csv(filtered_opportunities)
            save_to_html(filtered_opportunities)
            print('Job opportunities have been saved.')
        else:
            print("No oposiciones found for Alicante/Alacant")
    else:
        print('Failed to fetch data from BOE API')

if __name__ == '__main__':
    main()