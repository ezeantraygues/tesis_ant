# # Class to interact with gdrive to save/download files
# #TODO: implement class to communicate with gdrive
# class GdriveManager:

#     def put_item(item):
#         pass
import os
import shutil

class GdriveManager:
    """Clase para gestionar archivos en la carpeta sincronizada de Google Drive"""

    def __init__(self, base_path: str):
        self.base_path = base_path

    def put_item(self, local_file_path: str, drive_folder: str):
        destination_path = os.path.join(self.base_path, drive_folder, os.path.basename(local_file_path))
        shutil.copy(local_file_path, destination_path)
        print(f"Archivo {local_file_path} movido a {destination_path}")
        return destination_path

    def list_files(self, drive_folder: str):
        folder_path = os.path.join(self.base_path, drive_folder)
        return [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

    def download_item(self, drive_file_path: str, destination: str):
        shutil.copy(drive_file_path, destination)
        print(f"Archivo {drive_file_path} descargado a {destination}")

# Uso del GdriveManager con rutas corregidas
gdrive = GdriveManager("G:/Mi unidad")

# Subir un PDF
pdf_path = r"C:\Users\ezean\OneDrive\Escritorio\pdf_de_prueba\prueba.pdf"
gdrive.put_item(pdf_path, "informes_pdfs")

# Listar PDFs en la carpeta 'informes_pdfs'
archivos = gdrive.list_files("informes_pdfs")
print("Archivos PDF en Google Drive:", archivos)

# Descargar un archivo (descomentarlo para probar)
# gdrive.download_item("G:/Mi unidad/informes_pdfs/prueba.pdf", r"C:\Users\ezean\OneDrive\Escritorio\pdf_de_prueba\prueba_descargado.pdf")

#-----------------------------------------------------------------------------------------------------------

# from googleapiclient.discovery import build
# from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
# from google.oauth2 import service_account
# import io

# class GdriveManager:
#     """Clase para interactuar con Google Drive para guardar/descargar archivos"""

#     def __init__(self, credentials_json: str):
#         """
#         Inicializa la conexión con Google Drive usando credenciales de servicio.

#         :param credentials_json: Ruta al archivo JSON con las credenciales del servicio.
#         """
#         creds = service_account.Credentials.from_service_account_file(credentials_json)
#         self.service = build('drive', 'v3', credentials=creds)

#     def put_item(self, file_path: str, folder_id: str = None):
#         """
#         Sube un archivo a Google Drive.

#         :param file_path: Ruta local del archivo a subir.
#         :param folder_id: ID de la carpeta en Google Drive donde se guardará el archivo (opcional).
#         :return: ID del archivo subido en Google Drive.
#         """
#         file_metadata = {'name': file_path.split("/")[-1]}  # Nombre del archivo en Google Drive
#         if folder_id:
#             file_metadata['parents'] = [folder_id]  # Si se especifica una carpeta, asignarla

#         media = MediaFileUpload(file_path, mimetype='application/pdf')  # Cambiar 'application/pdf' según el tipo de archivo
#         file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()

#         return file.get('id')  # Devolver el ID del archivo subido

#     def download_item(self, file_id: str, destination: str):
#         """
#         Descarga un archivo de Google Drive.

#         :param file_id: El ID del archivo a descargar en Google Drive.
#         :param destination: Ruta local donde se guardará el archivo descargado.
#         """
#         request = self.service.files().get_media(fileId=file_id)
#         fh = io.FileIO(destination, 'wb')  # Archivo donde se guardará la descarga

#         downloader = MediaIoBaseDownload(fh, request)
#         done = False
#         while not done:
#             status, done = downloader.next_chunk()
#             print(f"Descargando {int(status.progress() * 100)}% completado.")

#         fh.close()

#     def list_files(self, query: str = None):
#         """
#         Lista archivos en Google Drive con una consulta opcional.

#         :param query: Consulta para filtrar los archivos (opcional). Ejemplo: "mimeType='application/pdf'".
#         :return: Lista de archivos que coinciden con la consulta.
#         """
#         results = self.service.files().list(q=query, pageSize=10, fields="files(id, name)").execute()
#         files = results.get('files', [])
#         return files

# # Ejemplo de uso
# if __name__ == "__main__":
#     # Inicializa el gestor de Google Drive
#     gdrive_manager = GdriveManager('ruta/a/credenciales.json')

#     # Subir un archivo PDF
#     file_id = gdrive_manager.put_item('ruta/a/archivo.pdf')
#     print(f"Archivo subido con ID: {file_id}")

#     # Descargar un archivo
#     gdrive_manager.download_item(file_id, 'ruta/a/descarga/archivo.pdf')

#     # Listar archivos en Google Drive
#     files = gdrive_manager.list_files("mimeType='application/pdf'")
#     for file in files:
#         print(f"Archivo: {file['name']} (ID: {file['id']})")




#---------------------------------------------------------------------------------------------------------
#