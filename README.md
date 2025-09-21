# SG Album Downloader

Este es un script de Python para descargar álbumes de fotos completos del sitio web Suicide Girls. El script maneja el inicio de sesión de forma segura, encuentra todas las imágenes de un set específico y las empaqueta en un único archivo `.zip` para una fácil descarga.

---
### ## Características

* **Inicio de sesión seguro:** Solicita usuario y contraseña por terminal. La contraseña no se muestra en pantalla al escribirla.
* **Autenticación moderna:** Utiliza el flujo de inicio de sesión de la API del sitio, manejando cookies de sesión automáticamente.
* **Descarga de álbumes completos:** Analiza la página de un álbum para encontrar todas las URLs de las imágenes en alta resolución.
* **Empaquetado automático:** Guarda todas las imágenes descargadas en un archivo `.zip` convenientemente nombrado.
* **Nombrado inteligente:** El archivo `.zip` se nombra automáticamente usando el formato `NombreModelo_TituloSet.zip`.
* **Barra de progreso:** Muestra el progreso de la descarga en tiempo real en la terminal.

---
### ## Requisitos

* Python 3.6 o superior
* Las librerías de Python listadas en el archivo `requirements.txt`.

---
### ## Instalación

1.  **Clona o descarga este repositorio.**

2.  **Crea y activa un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    # En Windows
    .\venv\Scripts\activate
    # En macOS/Linux
    source venv/bin/activate
    ```

3.  **Instala las dependencias:**
    Abre una terminal en la carpeta del proyecto y ejecuta el siguiente comando para instalar las librerías necesarias:
    ```bash
    pip install -r requirements.txt
    ```

---
### ## Modo de Empleo

1.  **Ejecuta el script** desde tu terminal:
    ```bash
    python sg_downloader.py
    ```

2.  **Introduce tu nombre de usuario** de Suicide Girls cuando se te solicite y presiona Enter.

3.  **Introduce tu contraseña.** No verás los caracteres mientras escribes por seguridad. Presiona Enter.

4.  Si el inicio de sesión es exitoso, **pega la URL completa** del álbum que deseas descargar y presiona Enter.

5.  ¡Listo! El script comenzará a descargar las imágenes y a crear el archivo `.zip`. Cuando termine, lo encontrarás en la misma carpeta donde ejecutaste el script.

---
### ## Aviso Importante

Este script depende de la estructura actual del sitio web y la API de Suicide Girls. Si el sitio realiza cambios significativos, el script podría dejar de funcionar y necesitaría ser actualizado.

Por favor, usa esta herramienta de forma responsable y respetando los términos de servicio del sitio web.