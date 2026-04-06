import requests
import json
import csv
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

# Constants
BOE_API_URL = 'https://api.boe.es/v1/boe'
OUTPUT_JSON = 'job_opportunities.json'
OUTPUT_CSV = 'job_opportunities.csv'
OUTPUT_HTML = 'job_opportunities.html'

# Fetch job opportunities data from BOE API

def fetch_job_opportunities():
    response = requests.get(BOE_API_URL)
    if response.status_code == 200:
        return response.json()  # Return JSON data
    else:
        print('Error fetching data from BOE API')
        return None

# Validate URLs

def validate_link(link):
    try:
        response = requests.head(link, allow_redirects=True)
        return response.status_code == 200
    except requests.RequestException:
        return False

# Filter job opportunities by date

def filter_by_date(opportunities, date):
    filtered_opportunities = []
    for opp in opportunities:
        opp_date = datetime.strptime(opp['date'], '%Y-%m-%d')
        if opp_date >= date:
            filtered_opportunities.append(opp)
    return filtered_opportunities

# Save data to JSON

def save_to_json(data):
    with open(OUTPUT_JSON, 'w') as json_file:
        json.dump(data, json_file, indent=4)

# Save data to CSV

def save_to_csv(data):
    with open(OUTPUT_CSV, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(['Title', 'Link', 'Date'])  # Header
        for item in data:
            writer.writerow([item['title'], item['link'], item['date']])

# Save data to HTML

def save_to_html(data):
    with open(OUTPUT_HTML, 'w') as html_file:
        html_file.write('<html><body><table>')
        html_file.write('<tr><th>Title</th><th>Link</th><th>Date</th></tr>')
        for item in data:
            html_file.write(f'<tr><td>{item['title']}</td><td><a href="{item['link']}">{item['link']}</a></td><td>{item['date']}</td></tr>')
        html_file.write('</table></body></html>')

# Main function

def main():
    # Set the date filter (e.g., opportunities from the last 30 days)
    date_filter = datetime.now() - timedelta(days=30)

    # Fetch opportunities
    opportunities = fetch_job_opportunities()
    if opportunities:
        # Validate links and filter by date
        valid_opportunities = [opp for opp in opportunities if validate_link(opp['link'])]
        filtered_opportunities = filter_by_date(valid_opportunities, date_filter)

        # Save the results
        save_to_json(filtered_opportunities)
        save_to_csv(filtered_opportunities)
        save_to_html(filtered_opportunities)
        print('Job opportunities have been saved.')

if __name__ == '__main__':
    main()