from flask import Flask, render_template, jsonify
from jobs_scraper import get_all_jobs_data
from notification_system import check_and_notify_jobs
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    """Home page with all public job offers in Alicante"""
    data = get_all_jobs_data()

    # Verificar y enviar notificaciones de jobs nuevos
    check_and_notify_jobs(data)

    return render_template('index.html', jobs=data['jobs'], total=data['total'])

@app.route('/api/jobs')
def get_jobs_api():
    """API endpoint for jobs data"""
    data = get_all_jobs_data()
    return jsonify(data)

@app.route('/api/oposiciones')
def get_oposiciones_api():
    """Legacy API endpoint for backward compatibility"""
    data = get_all_jobs_data()
    return jsonify(data)

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/sources')
def sources():
    """Sources information page"""
    return render_template('sources.html')

@app.route('/comunicacion')
def comunicacion():
    """Communication positions specialized page"""
    data = get_all_jobs_data()

    # Filter only communication jobs
    communication_jobs = [job for job in data['jobs'] if job.get('categoria') == 'Comunicación']
    communication_data = {
        'jobs': communication_jobs,
        'total': len(communication_jobs)
    }

    # Check and notify about new communication jobs
    check_and_notify_jobs(communication_data)

    return render_template('comunicacion.html', jobs=communication_jobs, total=len(communication_jobs))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)