#!/usr/bin/env python3
"""
Script para probar el envío de notificaciones por email
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from notification_system import notification_system

def test_email_notification():
    """Enviar una notificación de prueba muy simple"""

    # Email muy simple para probar SMTP
    test_jobs = [
        {
            'titulo': 'Prueba - Tecnico de Comunicacion',
            'fecha_publicacion': '20260408',
            'fuente': 'Ayuntamiento Alicante',
            'tipo': 'Funcionariado',
            'url_html': 'https://www.alicante.es/empleo',
            'plazo_abierto': True,
            'categoria': 'Comunicacion',
            'identificador': 'TEST-001',
            'bases': 'BASES DE PRUEBA: Esta es una convocatoria de prueba para verificar el sistema de email.'
        }
    ]

    print("Enviando email de prueba simple...")
    print("Destinatarios: salvazz@gmail.com")
    print("Ofertas de prueba: {}".format(len(test_jobs)))

    # Enviar notificación
    success = notification_system.send_notification(test_jobs)

    if success:
        print("Email de prueba enviado exitosamente!")
        print("Revisa tu bandeja de entrada en salvazz@gmail.com")
    else:
        print("Error al enviar el email de prueba")
        print("Revisa la configuracion SMTP en .env.local")

if __name__ == "__main__":
    test_email_notification()