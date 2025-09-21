import requests
import zipfile
import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import getpass

def login_to_sg_api(session, username, password):
    """
    Inicia sesión en la API v3 de Suicide Girls. Un código 204 indica éxito.
    """
    login_api_url = 'https://api.suicidegirls.com/v3/auth/login/'
    payload = {
        'username': username,
        'password': password
    }
    
    try:
        print("-> Conectando con la API para iniciar sesión...")
        response = session.post(login_api_url, json=payload)
        
        if response.status_code == 204:
            print("-> Sesión iniciada con éxito.")
            return True
        else:
            print(f"Error en el inicio de sesión: Código {response.status_code} - {response.text}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error durante la conexión a la API: {e}")
        return False

def get_album_info_and_images(session, album_url):
    """
    Usa la sesión con la cookie para obtener la información y las URLs de las imágenes.
    """
    print("-> Obteniendo información del álbum...")
    try:
        response = session.get(album_url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        path_parts = urlparse(album_url).path.strip('/').split('/')
        girl_name = path_parts[1] if len(path_parts) > 1 else "unknown_model"
        
        # --- LÍNEA CORREGIDA ---
        # Obtenemos el nombre del set directamente de la URL, que es más confiable.
        # Ejemplo: /girls/babis/album/5215230/slippery-floor -> path_parts[-1] es "slippery-floor"
        set_title = path_parts[-1] if len(path_parts) > 4 else "unknown_set"

        image_urls = []
        photo_containers = soup.find_all(class_='photo-container')
        for container in photo_containers:
            link = container.find('a')
            if link and link.has_attr('href'):
                image_urls.append(link['href'])
                
        if not image_urls:
            print("¡Advertencia! No se encontraron imágenes. ¿La URL es correcta y tienes acceso al álbum?")
            return None, None, None

        print(f"-> Modelo: {girl_name}, Set: {set_title}")
        print(f"-> Se encontraron {len(image_urls)} imágenes.")
        
        return girl_name, set_title, image_urls

    except requests.exceptions.RequestException as e:
        print(f"Error al acceder a la URL del álbum: {e}")
        return None, None, None

def download_and_zip_images(session, girl_name, set_title, image_urls):
    """
    Descarga las imágenes y las guarda en un .zip dentro de la carpeta 'Downloads'.
    """
    download_folder = "Downloads"
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)
        print(f"-> Carpeta '{download_folder}' creada.")

    safe_set_title = "".join([c for c in set_title if c.isalnum() or c in (' ', '-')]).rstrip()
    zip_filename = f"{girl_name}_{safe_set_title}.zip"
    
    zip_filepath = os.path.join(download_folder, zip_filename)
    
    total_images = len(image_urls)
    
    print(f"\nCreando archivo: {zip_filepath}")

    try:
        with zipfile.ZipFile(zip_filepath, 'w') as zipf:
            for i, img_url in enumerate(image_urls):
                try:
                    progress = (i + 1) / total_images * 100
                    print(f"  Descargando imagen {i+1}/{total_images} ({progress:.1f}%)", end='\r')
                    
                    img_response = session.get(img_url, stream=True)
                    img_response.raise_for_status()
                    
                    filename_in_zip = f"{str(i+1).zfill(2)}.jpg"
                    zipf.writestr(filename_in_zip, img_response.content)

                except requests.exceptions.RequestException as e:
                    print(f"\nError al descargar {img_url}: {e}")
                    continue

        print(f"\n\n¡Descarga completada! El archivo se guardó como '{zip_filepath}'")

    except Exception as e:
        print(f"\nOcurrió un error al crear el archivo zip: {e}")


if __name__ == "__main__":
    username = input("Introduce tu nombre de usuario de Suicide Girls: ")
    password = getpass.getpass("Introduce tu contraseña (no se mostrará): ")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    with requests.Session() as session:
        session.headers.update(headers)
        
        if login_to_sg_api(session, username, password):
            while True:
                album_url = input("\nIntroduce la URL del álbum de Suicide Girls: ")
                if album_url:
                    girl, title, images = get_album_info_and_images(session, album_url)
                    if girl and title and images:
                        download_and_zip_images(session, girl, title, images)
                
                another = input("\n¿Deseas descargar otro álbum? (s/n): ").lower()
                if another not in ['s', 'si', 'y', 'yes']:
                    print("¡Hasta luego!")
                    break