from flask import Flask, render_template, jsonify
from jobs_scraper import get_all_jobs_data
from notification_system import check_and_notify_jobs, JobNotificationSystem
import json
from datetime import datetime
import logging
from config import Config

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config.from_object(Config)

# Initialize notification system with config
notification_system = JobNotificationSystem(app.config)

@app.route('/')
def home():
    """Home page with all public job offers in Alicante"""
    try:
        data = get_all_jobs_data()

        # Filter out portal/general website listings - only show actual job offers
        filtered_jobs = [job for job in data['jobs'] if not (
            'Portal de empleo' in job['titulo'] or
            'Web municipal' in job['titulo'] or
            'Sistema' in job['titulo'] or
            'temporalmente no disponible' in job['titulo']
        )]

        # Verificar y enviar notificaciones de jobs nuevos
        check_and_notify_jobs({'jobs': filtered_jobs})

        return render_template('index.html', jobs=filtered_jobs, total=len(filtered_jobs))
    except Exception as e:
        logger.error(f"Error loading home page: {e}")
        return render_template('index.html', jobs=[], total=0, error="Error loading jobs data")

@app.route('/api/jobs')
def get_jobs_api():
    """API endpoint for jobs data"""
    try:
        data = get_all_jobs_data()
        return jsonify(data)
    except Exception as e:
        logger.error(f"Error in jobs API: {e}")
        return jsonify({'jobs': [], 'total': 0, 'error': 'Failed to fetch jobs data'}), 500

@app.route('/api/oposiciones')
def get_oposiciones_api():
    """Legacy API endpoint for backward compatibility"""
    data = get_all_jobs_data()
    return jsonify(data)

@app.route('/comunicacion')
def comunicacion():
    """Communication jobs page"""
    try:
        data = get_all_jobs_data()

        # Filter for communication jobs only
        communication_jobs = [job for job in data['jobs'] if
                            'comunicacion' in job.get('categoria', '').lower() or
                            'comunicacion' in job.get('titulo', '').lower() or
                            'periodista' in job.get('titulo', '').lower() or
                            'prensa' in job.get('titulo', '').lower() or
                            'community manager' in job.get('titulo', '').lower()]

        return render_template('comunicacion.html', jobs=communication_jobs, total=len(communication_jobs))
    except Exception as e:
        logger.error(f"Error loading communication page: {e}")
        return render_template('comunicacion.html', jobs=[], total=0, error="Error loading communication jobs")

@app.route('/sources')
def sources():
    """Sources information page"""
    return render_template('sources.html')

@app.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@app.route('/test-email')
def test_email():
    """Test email notifications - only for development"""
    # Crear una oferta de prueba
    test_jobs = [
        {
            'titulo': 'TEST - Tecnico Superior de Comunicacion',
            'fecha_publicacion': '20260408',
            'fuente': 'Ayuntamiento de Alicante',
            'tipo': 'Funcionariado',
            'url_html': 'https://oposiciones-alicante.vercel.app/comunicacion',
            'plazo_abierto': True,
            'categoria': 'Comunicacion',
            'identificador': 'TEST-EMAIL-001',
            'bases': 'Esta es una prueba del sistema de notificaciones por email.'
        }
    ]

    success = notification_system.send_notification(test_jobs)

    if success:
        return "<h1>✅ Email enviado correctamente!</h1><p>Revisa tu bandeja de entrada.</p>"
    else:
        return "<h1>❌ Error al enviar email</h1><p>Revisa la configuración en Vercel.</p>"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)