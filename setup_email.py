#!/usr/bin/env python3
"""
Script para configurar las variables de entorno de email en Vercel
Ejecuta este script para obtener los comandos exactos para configurar Vercel
"""

import os
import getpass

def generate_vercel_commands():
    """Genera los comandos para configurar Vercel"""

    print("🔧 CONFIGURACIÓN DE EMAIL PARA VERCEL")
    print("=" * 50)
    print()

    print("Para configurar las notificaciones por email en Vercel, necesitas:")
    print("1. Una cuenta de Gmail (recomendado)")
    print("2. Generar una 'Contraseña de aplicación' en Gmail")
    print("3. Ejecutar los comandos que se muestran abajo")
    print()

    print("📧 PASO 1: Configurar Gmail")
    print("-" * 30)
    print("1. Ve a: https://myaccount.google.com/security")
    print("2. Activa la 'Verificación en 2 pasos'")
    print("3. Ve a 'Contraseñas de aplicación'")
    print("4. Selecciona 'Correo' y 'Otro (nombre personalizado)'")
    print("5. Escribe: 'EmpleoPublicoAlicante'")
    print("6. Copia la contraseña generada (16 caracteres)")
    print()

    # Pedir credenciales de forma segura
    sender_email = input("Ingresa tu email de Gmail: ").strip()
    if not sender_email:
        sender_email = "tu-email@gmail.com"

    print("Ingresa la contraseña de aplicación de Gmail (16 caracteres):")
    print("⚠️  IMPORTANTE: Asegúrate de copiarla exactamente como Gmail te la dio")
    sender_password = getpass.getpass("Contraseña de aplicación: ")

    if not sender_password:
        sender_password = "tu-app-password"

    # Confirmar destinatarios
    recipient_emails = "salvazz@gmail.com,lucasaliagadelaencarnacion@gmail.com"
    print(f"Destinatarios configurados: {recipient_emails}")
    change_recipients = input("¿Quieres cambiar los destinatarios? (s/n): ").lower().strip()
    if change_recipients == 's':
        recipient_emails = input("Ingresa los emails separados por comas: ").strip()

    print()
    print("🚀 PASO 2: Comandos para Vercel")
    print("-" * 30)
    print("Ve a tu dashboard de Vercel y ejecuta estos comandos en la terminal:")
    print()

    commands = [
        f"vercel env add SMTP_SERVER",
        f"vercel env add SMTP_PORT",
        f"vercel env add SENDER_EMAIL",
        f"vercel env add SENDER_PASSWORD",
        f"vercel env add RECIPIENT_EMAILS"
    ]

    for i, cmd in enumerate(commands, 1):
        print(f"{i}. {cmd}")

    print()
    print("📝 VALORES A INGRESAR:")
    print("-" * 25)
    print(f"SMTP_SERVER: smtp.gmail.com")
    print(f"SMTP_PORT: 587")
    print(f"SENDER_EMAIL: {sender_email}")
    print(f"SENDER_PASSWORD: {sender_password}")
    print(f"RECIPIENT_EMAILS: {recipient_emails}")
    print()

    print("✅ PASO 3: Verificar configuración")
    print("-" * 30)
    print("Después de configurar todas las variables:")
    print("1. Haz un commit y push a GitHub")
    print("2. Vercel redeployará automáticamente")
    print("3. Las notificaciones por email estarán activas")
    print()

    print("🧪 PASO 4: Probar las notificaciones")
    print("-" * 30)
    print("Para probar que funciona, ejecuta:")
    print("python test_email.py")
    print()

    print("📧 FUNCIONAMIENTO")
    print("-" * 15)
    print("Cada vez que se detecten nuevas ofertas, recibirás emails con:")
    print("• Bases completas de las convocatorias")
    print("• Enlaces directos a PDFs oficiales")
    print("• Información detallada de requisitos y plazos")
    print("• Categorización por tipo de puesto")
    print()

    print("🎉 ¡Configuración completada!")
    print("Tu sistema de notificaciones estará listo una vez que Vercel redeploye.")

if __name__ == "__main__":
    try:
        generate_vercel_commands()
    except KeyboardInterrupt:
        print("\n\nConfiguración cancelada.")
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Si tienes problemas, configura manualmente las variables en el dashboard de Vercel.")