# # Class to interact with gdrive to save/download files
# #TODO: implement class to communicate with gdrive
# class GdriveManager:

#     def put_item(item):
#         pass
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2 import service_account
import io

class GdriveManager:
    """Clase para interactuar con Google Drive para guardar/descargar archivos"""

    def __init__(self, credentials_json: str):
        """
        Inicializa la conexión con Google Drive usando credenciales de servicio.

        :param credentials_json: Ruta al archivo JSON con las credenciales del servicio.
        """
        creds = service_account.Credentials.from_service_account_file(credentials_json)
        self.service = build('drive', 'v3', credentials=creds)

    def put_item(self, file_path: str, folder_id: str = None):
        """
        Sube un archivo a Google Drive.

        :param file_path: Ruta local del archivo a subir.
        :param folder_id: ID de la carpeta en Google Drive donde se guardará el archivo (opcional).
        :return: ID del archivo subido en Google Drive.
        """
        file_metadata = {'name': file_path.split("/")[-1]}  # Nombre del archivo en Google Drive
        if folder_id:
            file_metadata['parents'] = [folder_id]  # Si se especifica una carpeta, asignarla

        media = MediaFileUpload(file_path, mimetype='application/pdf')  # Cambiar 'application/pdf' según el tipo de archivo
        file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

        return file.get('id')  # Devolver el ID del archivo subido

    def download_item(self, file_id: str, destination: str):
        """
        Descarga un archivo de Google Drive.

        :param file_id: El ID del archivo a descargar en Google Drive.
        :param destination: Ruta local donde se guardará el archivo descargado.
        """
        request = self.service.files().get_media(fileId=file_id)
        fh = io.FileIO(destination, 'wb')  # Archivo donde se guardará la descarga

        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while not done:
            status, done = downloader.next_chunk()
            print(f"Descargando {int(status.progress() * 100)}% completado.")

        fh.close()

    def list_files(self, query: str = None):
        """
        Lista archivos en Google Drive con una consulta opcional.

        :param query: Consulta para filtrar los archivos (opcional). Ejemplo: "mimeType='application/pdf'".
        :return: Lista de archivos que coinciden con la consulta.
        """
        results = self.service.files().list(q=query, pageSize=10, fields="files(id, name)").execute()
        files = results.get('files', [])
        return files
    
"""ej de uso"""

"""Supongamos que tienes un archivo credentials.json para las credenciales de servicio, así podrías usar esta clase:"""
# gdrive_manager = GdriveManager('path/to/credentials.json')

# # Subir un archivo
# file_id = gdrive_manager.put_item('path/to/local/file.pdf')

# # Descargar un archivo
# gdrive_manager.download_item(file_id, 'path/to/download/file.pdf')

# # Listar archivos en Google Drive
# files = gdrive_manager.list_files("mimeType='application/pdf'")
# for file in files:
#     print(f"Archivo: {file['name']} (ID: {file['id']})")
"""Con esto podrás manejar archivos en Google Drive directamente desde tu código. Recuerda manejar bien las credenciales y asegurar que solo usuarios autorizados tengan acceso a ellas."""
