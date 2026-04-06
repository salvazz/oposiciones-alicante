# Instrucciones para desplegar la aplicación web

Para desplegar la aplicación web, sigue los siguientes pasos:

1. **Clona el repositorio**:
   ```bash
   git clone https://github.com/salvazz/oposiciones-alicante.git
   cd oposiciones-alicante
   ```

2. **Instala las dependencias**:
   Asegúrate de tener instalado [Node.js](https://nodejs.org/) y luego ejecuta:
   ```bash
   npm install
   ```

3. **Configura las variables de entorno**:
   Crea un archivo `.env` en la raíz del proyecto y añade las siguientes variables:
   ```
   DB_HOST=localhost
   DB_USER=tu_usuario
   DB_PASS=tu_contraseña
   ```

4. **Ejecuta la aplicación**:
   ```bash
   npm start
   ```

5. **Accede a la aplicación**:
   Abre tu navegador y ve a `http://localhost:3000` para ver la aplicación en funcionamiento.

Si encuentras algún problema, consulta la documentación o contacta con el soporte.