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

@app.route('/test-email')
def test_email():
    """Test email notifications - only for development"""
    from notification_system import notification_system

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