# Empleo Público Alicante

Aplicación web completa que muestra **todas las ofertas de empleo público** disponibles en la provincia de Alicante, obtenidas automáticamente de **5 fuentes oficiales diferentes**:

- 🏛️ **BOE** - Boletín Oficial del Estado (Administración General)
- 🏛️ **DOGV** - Diario Oficial de la Generalitat Valenciana
- 🏛️ **Diputación de Alicante** - Administración Provincial
- 🏛️ **Ayuntamientos** - 10 municipios principales de Alicante
- 🏛️ **Unión Europea** - EPSO y EUR-Lex

## 🚀 Características Principales

- ✅ **5 fuentes oficiales** de empleo público monitorizadas
- ✅ **Búsqueda automática** diaria de nuevas ofertas
- ✅ **Solo muestra ofertas con plazo abierto**
- ✅ **Interfaz moderna** con filtros y búsqueda en tiempo real
- ✅ **Notificaciones por email** automáticas de nuevas ofertas
- ✅ **Hosting gratuito** e ilimitado
- ✅ **Responsive design** para móviles y tablets

## 📧 Sistema de Notificaciones

**Alertas automáticas por email** cuando se publiquen nuevas ofertas:

- 📬 **Destinatarios:** salvazz@gmail.com, lucasaliagadelaencarnacion@gmail.com
- 📬 **Contenido:** Email HTML con detalles completos de las nuevas ofertas
- 📬 **Frecuencia:** Automática al detectar nuevas publicaciones
- 📬 **Enlaces directos:** Acceso inmediato a las convocatorias oficiales

## 🛠️ Desarrollo Local

### Requisitos previos
- Python 3.8+
- pip

### Instalación

1. **Clona el repositorio:**
   ```bash
   git clone https://github.com/salvazz/oposiciones-alicante.git
   cd oposiciones-alicante
   ```

2. **Configura variables de entorno** (opcional para notificaciones):
   ```bash
   cp .env.example .env
   # Edita .env con tus credenciales de email
   ```

3. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```

5. **Accede a la aplicación:**
   Abre tu navegador en `http://localhost:5000`

## 🌐 Despliegue en Hosting Gratuito

### Opción 1: Vercel (Recomendado) ⭐

1. **Instala Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Despliega:**
   ```bash
   cd oposiciones-alicante
   vercel
   ```

3. **Configura variables de entorno** (para notificaciones):
   ```bash
   vercel env add SMTP_SERVER
   vercel env add SMTP_PORT
   vercel env add SENDER_EMAIL
   vercel env add SENDER_PASSWORD
   vercel env add RECIPIENT_EMAILS
   ```

### Opción 2: Railway

1. Ve a [Railway.app](https://railway.app)
2. Conecta tu repo `salvazz/oposiciones-alicante`
3. Railway detecta automáticamente Flask
4. Configura variables de entorno en el dashboard

### Opción 3: Render

1. Ve a [Render.com](https://render.com)
2. Crea nuevo Web Service
3. Conecta repo de GitHub
4. Configura:
   - **Runtime:** Python 3
   - **Build:** `pip install -r requirements-web.txt`
   - **Start:** `python app.py`

## 📊 API Endpoints

### Página Principal
```
GET /
```
Interfaz web completa con todas las ofertas activas.

### API JSON
```
GET /api/jobs
```
Devuelve todas las ofertas en formato JSON:
```json
{
  "jobs": [
    {
      "titulo": "Auxiliar Administrativo - Ayuntamiento de Alicante",
      "fecha_publicacion": "20260408",
      "fuente": "Ayuntamiento de Alicante",
      "tipo": "Empleo Municipal",
      "url_html": "https://www.alicante.es/empleo/...",
      "plazo_abierto": true,
      "categoria": "Administración Local"
    }
  ],
  "total": 15
}
```

### Páginas Adicionales
- `/sources` - Información detallada de todas las fuentes
- `/about` - Información del proyecto

## 🔧 Tecnologías Utilizadas

- **Backend:** Python Flask
- **Frontend:** Bootstrap 5, Animate.css, Font Awesome
- **Web Scraping:** Requests, BeautifulSoup4
- **Notificaciones:** SMTP (Gmail/Outlook)
- **Configuración:** python-dotenv
- **Hosting:** Vercel/Railway/Render

## 📋 Fuentes de Datos Monitorizadas

| Fuente | Estado | Descripción |
|--------|--------|-------------|
| **BOE** | ✅ Activo | Boletín Oficial del Estado |
| **DOGV** | 🔄 Desarrollo | Generalitat Valenciana |
| **Diputación** | ✅ Activo | Provincia de Alicante |
| **Ayuntamientos** | ✅ Activo | 10 municipios principales |
| **Unión Europea** | ✅ Activo | EPSO y EUR-Lex |

### Ayuntamientos Monitorizados:
- Alicante/Alacant, Elche/Elx, Torrevieja, Orihuela
- Benidorm, Alcoy/Alcoi, Villena, Elda
- San Vicente del Raspeig, Aspe

## ⚙️ Configuración de Email

Para activar las notificaciones automáticas:

1. **Crea un archivo `.env`:**
   ```bash
   SMTP_SERVER=smtp.gmail.com
   SMTP_PORT=587
   SENDER_EMAIL=tu-email@gmail.com
   SENDER_PASSWORD=tu-app-password
   RECIPIENT_EMAILS=salvazz@gmail.com,lucasaliagadelaencarnacion@gmail.com
   ```

2. **Para Gmail:** Genera una "Contraseña de aplicación"
   - Ve a [Google Account Settings](https://myaccount.google.com/security)
   - Activa 2FA
   - Genera contraseña de app

## 📝 Información Importante

⚠️ **Esta aplicación es únicamente informativa.** Siempre verifica:
- Información oficial en los enlaces proporcionados
- Bases de las convocatorias
- Fechas límite de presentación
- Requisitos específicos

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m 'Añade nueva funcionalidad'`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.

---

**🚀 Aplicación desplegada en:** https://oposiciones-alicante.vercel.app/