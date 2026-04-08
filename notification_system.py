import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import os
from datetime import datetime
try:
    from dotenv import load_dotenv
except ImportError:
    # Fallback si no está instalado dotenv
    def load_dotenv():
        pass

# Cargar variables de entorno
load_dotenv()

class JobNotificationSystem:
    def __init__(self):
        # Configuración de email - usar variables de entorno para seguridad
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.sender_email = os.getenv('SENDER_EMAIL', 'tu-email@gmail.com')
        self.sender_password = os.getenv('SENDER_PASSWORD', 'tu-password')

        # Recipients desde variable de entorno
        recipient_str = os.getenv('RECIPIENT_EMAILS', 'salvazz@gmail.com,lucasaliagadelaencarnacion@gmail.com')
        self.recipient_emails = [email.strip() for email in recipient_str.split(',')]

        # Archivo para tracking de notificaciones enviadas
        self.tracking_file = 'sent_notifications.json'
        self.load_sent_notifications()

    def load_sent_notifications(self):
        """Cargar notificaciones ya enviadas"""
        try:
            if os.path.exists(self.tracking_file):
                with open(self.tracking_file, 'r') as f:
                    self.sent_notifications = json.load(f)
            else:
                self.sent_notifications = {}
        except:
            self.sent_notifications = {}

    def save_sent_notifications(self):
        """Guardar notificaciones enviadas"""
        try:
            with open(self.tracking_file, 'w') as f:
                json.dump(self.sent_notifications, f, indent=2)
        except Exception as e:
            print("Error saving notifications: {}".format(str(e)))

    def is_notification_sent(self, job_id):
        """Verificar si ya se envió notificación para este job"""
        return job_id in self.sent_notifications

    def mark_notification_sent(self, job_id, job_title):
        """Marcar notificación como enviada"""
        self.sent_notifications[job_id] = {
            'title': job_title,
            'sent_date': datetime.now().isoformat(),
            'recipients': self.recipient_emails
        }
        self.save_sent_notifications()

    def create_notification_email(self, new_jobs):
        """Crear el contenido del email de notificación"""
        subject = "🔔 Nuevas ofertas de empleo público en Alicante"

        # Crear mensaje HTML
        html_content = """
        <html>
        <head>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                .header { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                         color: white; padding: 20px; border-radius: 10px; margin-bottom: 20px; }
                .job-card { border: 1px solid #ddd; border-radius: 8px; padding: 15px;
                           margin-bottom: 15px; background: #f9f9f9; }
                .job-title { font-weight: bold; color: #333; margin-bottom: 8px; }
                .job-meta { color: #666; font-size: 14px; margin-bottom: 8px; }
                .job-link { display: inline-block; background: #28a745; color: white;
                           padding: 8px 15px; text-decoration: none; border-radius: 5px; }
                .footer { margin-top: 30px; padding-top: 20px; border-top: 1px solid #ddd;
                         color: #666; font-size: 12px; }
            </style>
        </head>
        <body>
            <div class="header">
                <h2>🔔 Nuevas Ofertas de Empleo Público</h2>
                <p>Se han encontrado <strong>{}</strong> nuevas ofertas en la provincia de Alicante</p>
            </div>
        """.format(len(new_jobs))

        for job in new_jobs:
            html_content += """
            <div class="job-card">
                <div class="job-title">📋 {}</div>
                <div class="job-meta">
                    <strong>Fuente:</strong> {}<br>
                    <strong>Categoría:</strong> {}<br>
                    <strong>Fecha:</strong> {}<br>
                    <strong>Tipo:</strong> {}
                </div>
                <a href="{}" class="job-link">Ver oferta completa →</a>
            </div>
            """.format(
                job['titulo'],
                job['fuente'],
                job['categoria'],
                job['fecha_publicacion'],
                job['tipo'],
                job['url_html']
            )

        html_content += """
            <div class="footer">
                <p>
                    Este email fue enviado automáticamente por el sistema de notificaciones
                    de Oposiciones Alicante.<br>
                    <a href="https://oposiciones-alicante.vercel.app">Visitar la web completa</a>
                </p>
            </div>
        </body>
        </html>
        """

        return subject, html_content

    def send_notification(self, new_jobs):
        """Enviar notificación por email"""
        if not new_jobs:
            print("No new jobs to notify about")
            return False

        if not self.sender_email or not self.sender_password:
            print("Email credentials not configured")
            return False

        try:
            # Crear mensaje
            subject, html_content = self.create_notification_email(new_jobs)

            # Configurar servidor SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.sender_email, self.sender_password)

            # Enviar a cada destinatario
            for recipient in self.recipient_emails:
                msg = MIMEMultipart('alternative')
                msg['Subject'] = subject
                msg['From'] = self.sender_email
                msg['To'] = recipient

                # Adjuntar contenido HTML
                html_part = MIMEText(html_content, 'html')
                msg.attach(html_part)

                # Enviar email
                server.sendmail(self.sender_email, recipient, msg.as_string())
                print("Notification sent to {}".format(recipient))

            server.quit()
            return True

        except Exception as e:
            print("Error sending notification: {}".format(str(e)))
            return False

    def check_and_notify_new_jobs(self, current_jobs):
        """Verificar jobs nuevos y enviar notificaciones"""
        new_jobs = []

        for job in current_jobs:
            # Crear ID único para el job
            job_id = "{}_{}_{}".format(
                job.get('identificador', job['titulo'][:50].replace(' ', '_')),
                job['fuente'].replace(' ', '_'),
                job['fecha_publicacion']
            )

            if not self.is_notification_sent(job_id):
                new_jobs.append(job)
                self.mark_notification_sent(job_id, job['titulo'])

        if new_jobs:
            print("Found {} new jobs, sending notifications...".format(len(new_jobs)))
            success = self.send_notification(new_jobs)
            if success:
                print("Notifications sent successfully!")
            else:
                print("Failed to send notifications")
        else:
            print("No new jobs found")

        return len(new_jobs)

# Función global para usar en la aplicación
notification_system = JobNotificationSystem()

def check_and_notify_jobs(jobs_data):
    """Función wrapper para verificar y notificar jobs nuevos"""
    return notification_system.check_and_notify_new_jobs(jobs_data['jobs'])