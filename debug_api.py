import requests
import json
from datetime import datetime

BASE_BOE_API_URL = 'https://www.boe.es/datosabiertos/api'

def debug_api():
    headers = {'Accept': 'application/json'}
    today = datetime.now().strftime('%Y%m%d')
    url = f"{BASE_BOE_API_URL}/boe/sumario/{today}"
    
    print(f"Fetching from: {url}")
    response = requests.get(url, headers=headers, timeout=10)
    
    if response.status_code == 200:
        data = response.json()
        print("Response structure:")
        print(json.dumps(data, indent=2)[:2000])  # First 2000 chars
        print("\n..." if len(json.dumps(data, indent=2)) > 2000 else "")
        
        # Try to extract some basic info
        if 'data' in data and 'sumario' in data['data']:
            sumario = data['data']['sumario']
            print(f"\nSumario fecha: {sumario.get('metadatos', {}).get('fecha_publicacion')}")
            print(f"Número de diario: {sumario.get('diario', [{}])[0].get('numero') if sumario.get('diario') else 'N/A'}")
            
            # Look for oposiciones in the content
            diario_content = sumario.get('diario', [])
            for i, diario_item in enumerate(diario_content[:3]):  # First 3 diario items
                print(f"\nDiario {i+1}:")
                print(f"  Número: {diario_item.get('numero')}")
                secciones = diario_item.get('seccion', [])
                for j, seccion in enumerate(secciones[:2]):  # First 2 secciones
                    print(f"  Sección {j+1}: {seccion.get('nombre', 'N/A')}")
                    departamentos = seccion.get('departamento', [])
                    for k, dept in enumerate(departamentos[:2]):  # First 2 departamentos
                        print(f"    Departamento {k+1}: {dept.get('nombre', 'N/A')}")
                        if 'epigrafe' in dept.get('texto', {}):
                            epigrafes = dept['texto']['epigrafe']
                            for l, epigrafe in enumerate(epigrafes[:2]):  # First 2 epigrafes
                                print(f"      Epígrafe {l+1}: {epigrafe.get('nombre', 'N/A')}")
                                if 'item' in epigrafe:
                                    item = epigrafe['item']
                                    print(f"        Item: {item.get('titulo', 'N/A')[:100]}...")
    else:
        print(f"Error: {response.status_code}")
        print(response.text[:500])

if __name__ == "__main__":
    debug_api()