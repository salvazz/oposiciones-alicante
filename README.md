# Oposiciones Alicante

Aplicación web que muestra plazas de **Auxiliar Administrativo** disponibles en la provincia de Alicante, obtenidas automáticamente del Boletín Oficial del Estado (BOE).

## 🚀 Características

- ✅ Búsqueda automática de plazas de Auxiliar Administrativo en Alicante
- ✅ Solo muestra convocatorias con **plazo de presentación abierto**
- ✅ Datos actualizados diariamente desde el BOE
- ✅ Interfaz web moderna y responsive
- ✅ Enlaces directos a la documentación oficial
- ✅ Funcionalidad de búsqueda en tiempo real

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

2. **Instala las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Ejecuta la aplicación:**
   ```bash
   python app.py
   ```

4. **Accede a la aplicación:**
   Abre tu navegador en `http://localhost:5000`

## 🌐 Despliegue en Hosting Gratuito

### Opción 1: Vercel (Recomendado)

1. **Instala Vercel CLI:**
   ```bash
   npm install -g vercel
   ```

2. **Despliega:**
   ```bash
   vercel
   ```

3. **Configura las variables de entorno** (si es necesario)

### Opción 2: Railway

1. Ve a [Railway.app](https://railway.app) y crea una cuenta
2. Conecta tu repositorio de GitHub
3. Railway detectará automáticamente la aplicación Flask
4. ¡Listo! Tu app estará online

### Opción 3: Render

1. Ve a [Render.com](https://render.com) y crea una cuenta
2. Crea un nuevo servicio web
3. Conecta tu repositorio de GitHub
4. Configura:
   - **Runtime:** Python 3
   - **Build Command:** `pip install -r requirements-web.txt`
   - **Start Command:** `python app.py`

## 📊 API

### Endpoint principal
```
GET /
```
Devuelve la página principal con todas las oposiciones activas.

### API JSON
```
GET /api/oposiciones
```
Devuelve los datos en formato JSON:
```json
{
  "oposiciones": [
    {
      "titulo": "Resolución de... Auxiliar Administrativo...",
      "fecha_publicacion": "20260408",
      "identificador": "BOE-A-2026-XXXX",
      "url_html": "https://www.boe.es/...",
      "url_pdf": "https://www.boe.es/...",
      "plazo_abierto": true
    }
  ],
  "total": 1
}
```

## 🔧 Tecnologías Utilizadas

- **Backend:** Python Flask
- **Frontend:** HTML5, CSS3, Bootstrap 5, JavaScript
- **Web Scraping:** Requests, BeautifulSoup4
- **Datos:** API del Boletín Oficial del Estado (BOE)
- **Hosting:** Vercel/Railway/Render (gratuito)

## 📝 Información Importante

⚠️ **Esta aplicación es únicamente informativa.** Siempre verifica la información oficial en los enlaces proporcionados y consulta las bases de las convocatorias.

## 🤝 Contribuir

Si encuentras algún problema o tienes sugerencias:

1. Abre un issue en este repositorio
2. Haz un fork del proyecto
3. Crea una rama para tu feature
4. Envía un pull request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT.