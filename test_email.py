#!/usr/bin/env python3
"""
Script para probar el envío de notificaciones por email
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from notification_system import notification_system

def test_email_notification():
    """Enviar una notificación de prueba con oferta simulada"""

    # Oferta simulada de comunicación
    test_jobs = [
        {
            'titulo': 'Técnico Superior de Comunicación - Ayuntamiento de Alicante',
            'fecha_publicacion': '20260408',
            'fuente': 'Ayuntamiento de Alicante',
            'tipo': 'Funcionariado',
            'url_html': 'https://www.alicante.es/empleo/tecnico-comunicacion-2026',
            'plazo_abierto': True,
            'categoria': 'Comunicación',
            'identificador': 'TEST-001',
            'bases': """
BASES DE LA CONVOCATORIA PARA LA PROVISIÓN DE PLAZA DE TÉCNICO SUPERIOR DE COMUNICACIÓN

1. OBJETO DE LA CONVOCATORIA
Provisión por el sistema de concurso-oposición de una plaza de Técnico Superior de Comunicación.

2. FUNCIONES DEL PUESTO
- Diseñar y ejecutar la estrategia de comunicación del Ayuntamiento
- Coordinar campañas de comunicación institucional
- Gestionar la imagen corporativa y marca municipal
- Elaborar planes de comunicación anuales
- Supervisar la producción de contenidos multimedia
- Gestionar crisis comunicativas
- Coordinar relaciones con medios de comunicación

3. REQUISITOS
- Titulación universitaria en Comunicación, Periodismo, Publicidad o similar
- Experiencia mínima de 3 años en puestos de comunicación
- Conocimientos avanzados en redes sociales y herramientas digitales
- Nivel C1 de valenciano

4. SISTEMA DE ACCESO
- Fase de concurso: valoración de méritos (hasta 60 puntos)
- Fase de oposición: prueba práctica y entrevista (hasta 40 puntos)

5. PLAZO DE PRESENTACIÓN
Del 8 de abril al 8 de mayo de 2026

6. DOCUMENTACIÓN A PRESENTAR
- Instancia de participación
- DNI/NIE
- Titulación académica
- Curriculum vitae detallado
- Certificados de experiencia laboral
- Justificante de pago de tasas (50€)

7. LUGAR DE PRESENTACIÓN
Registro General del Ayuntamiento de Alicante
Plaza del Ayuntamiento, 1
03002 Alicante

8. INFORMACIÓN ADICIONAL
Más información en www.alicante.es/empleo o teléfono 965123456
            """
        },
        {
            'titulo': 'Periodista - Gabinete de Prensa - Diputación de Alicante',
            'fecha_publicacion': '20260408',
            'fuente': 'Diputación de Alicante',
            'tipo': 'Funcionariado',
            'url_html': 'https://www.dip-alicante.es/empleo/periodista-gabinete-2026',
            'plazo_abierto': True,
            'categoria': 'Comunicación',
            'identificador': 'TEST-002',
            'bases': """
CONVOCATORIA PARA PROVISIÓN DE PLAZA DE PERIODISTA EN GABINETE DE PRENSA

1. DENOMINACIÓN DEL PUESTO
Periodista - Especialista en Comunicación Institucional

2. DEPENDENCIA ORGÁNICA
Gabinete de Comunicación - Diputación de Alicante

3. FUNCIONES PRINCIPALES
- Redactar notas de prensa y comunicados oficiales
- Gestionar entrevistas y ruedas de prensa
- Atender consultas de medios de comunicación
- Redactar discursos para autoridades provinciales
- Elaborar dossiers de prensa para eventos
- Mantener relación permanente con periodistas
- Gestionar la hemeroteca provincial

4. CONDICIONES DE ACCESO
- Licenciatura en Periodismo, Comunicación o similar
- Experiencia mínima de 2 años en medios de comunicación
- Conocimientos de legislación en materia de comunicación
- Nivel B2 de valenciano acreditado

5. FORMA DE ACCESO
- Concurso-oposición libre
- Valoración de méritos: 40 puntos
- Pruebas selectivas: 60 puntos

6. TEMPORALIZACIÓN
- Plazo de presentación: 15 días naturales desde publicación
- Fecha límite: 23 de abril de 2026

7. TRIBUNAL CALIFICADOR
- Presidente: Director/a de Comunicación
- Vocales: Técnicos superiores de comunicación
- Secretario: Letrado/a de la Diputación

8. DOCUMENTACIÓN
- Solicitud en modelo oficial
- DNI y copia compulsada
- Título académico compulsado
- Certificación de vida laboral
- Curriculum vitae
- Declaración responsable de no estar inhabilitado

9. LUGAR DE EXAMEN
Sede de la Diputación Provincial
Calle San Fernando, 6
03001 Alicante

10. RECURSOS
Contra la convocatoria: 1 mes desde publicación
Contra el acto de adjudicación: 1 mes desde notificación
            """
        }
    ]

    print("Enviando notificacion de prueba...")
    print("Destinatarios: salvazz@gmail.com")
    print("Ofertas de prueba: {}".format(len(test_jobs)))

    # Enviar notificación
    success = notification_system.send_notification(test_jobs)

    if success:
        print("Notificacion de prueba enviada exitosamente!")
        print("Revisa tu email salvazz@gmail.com")
    else:
        print("Error al enviar la notificacion de prueba")
        print("Verifica la configuracion de email en Vercel")

if __name__ == "__main__":
    test_email_notification()