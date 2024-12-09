from __future__ import print_function
import pickle
import os.path
import io

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.http import MediaIoBaseDownload, MediaFileUpload

# Class to interact with Google Drive API
class DriveAPI:
    global SCOPES

    # Define the scopes
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self):
        # Variable self.creds will store the user access token.
        # If no valid token is found, a new one will be created.
        self.creds = None

        # The file token.pickle stores the user's access and refresh tokens.
        # It is created automatically when the authorization flow completes for the first time.
        if os.path.exists("token.pickle"):
            with open("token.pickle", "rb") as token:
                self.creds = pickle.load(token)

        # If no valid credentials are available, request the user to log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    "src/common/credentials.json", SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save the access token in token.pickle file for future usage
            with open("token.pickle", "wb") as token:
                pickle.dump(self.creds, token)

        # Connect to the API service
        self.service = build("drive", "v3", credentials=self.creds)

    def listFolders(self):
        try:
            page_token = None
            folders = []
            while True:
                response = (
                    self.service.files()
                    .list(
                        q="mimeType='application/vnd.google-apps.folder'",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )

                for file in response.get("files", []):
                    folder_data = (file.get("name"), file.get("id"))
                    folders.append(folder_data)

                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    break

            return folders
        except Exception as e:
            print(str(e))
            return None

    def download_file(self, file_id, destination_path):
        """
        Downloads a file from Google Drive by its file ID.
        :param file_id: The ID of the file to download.
        :param destination_path: The local path where the file will be saved.
        """
        try:
            request = self.service.files().get_media(fileId=file_id)
            with io.FileIO(destination_path, "wb") as file_handle:
                downloader = MediaIoBaseDownload(file_handle, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    print(f"Download progress: {int(status.progress() * 100)}%")
            print(f"File downloaded successfully to: {destination_path}")
        except Exception as e:
            print(f"Error downloading file: {e}")


class Uploader(DriveAPI):
    def __init__(self):
        super(Uploader, self).__init__()

    def createFolder(self, folder_name, parent_folder_id=None):
        file_metadata = {
            "name": folder_name,
            "mimeType": "application/vnd.google-apps.folder",
        }
        if parent_folder_id:
            file_metadata["parents"] = [parent_folder_id]

        folder = self.service.files().create(body=file_metadata, fields="id").execute()
        return folder.get("id")

    def uploadFile(self, file_path, parent_folder_id=None):
        file_metadata = {"name": os.path.basename(file_path)}
        if parent_folder_id:
            file_metadata["parents"] = [parent_folder_id]

        media = MediaFileUpload(file_path, resumable=True)
        file = (
            self.service.files()
            .create(body=file_metadata, media_body=media, fields="id")
            .execute()
        )
        return file.get("id")

    def uploadFolder(self, folder_path, parent_folder_id=None, new_folder_name=None):
        # Use the new_folder_name if provided, otherwise use the local folder name
        folder_name = new_folder_name if new_folder_name else os.path.basename(folder_path)
        folder_id = self.createFolder(folder_name, parent_folder_id)
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                self.uploadFolder(item_path, folder_id)
            else:
                self.uploadFile(item_path, folder_id)
        return folder_id


# # This code comes from zdrive 2.1.5
# # The original library does not have the capability we needed so I get the code from the library and modify it to suit our needs.
# # Just a wrapper for the Google Drive API

# from __future__ import print_function
# import pickle
# import os.path
# import io

# from multiprocessing import Process
# from googleapiclient.discovery import build
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.http import MediaIoBaseDownload
# from googleapiclient.http import MediaFileUpload

# # # Class to interact with gdrive to save/download files
# import os
# import shutil


# try:
#     from signal import signal, SIGPIPE, SIG_DFL

#     signal(SIGPIPE, SIG_DFL)
# except ImportError:
#     pass


# class DriveAPI:
#     global SCOPES

#     # Define the scopes
#     SCOPES = ["https://www.googleapis.com/auth/drive"]

#     def __init__(self):

#         # Variable self.creds will
#         # store the user access token.
#         # If no valid token found
#         # we will create one.
#         self.creds = None

#         # The file token.pickle stores the
#         # user's access and refresh tokens. It is
#         # created automatically when the authorization
#         # flow completes for the first time.

#         # Check if file token.pickle exists
#         if os.path.exists("token.pickle"):
#             # Read the token from the file and
#             # store it in the variable self.creds
#             with open("token.pickle", "rb") as token:
#                 self.creds = pickle.load(token)

#         # If no valid credentials are available,
#         # request the user to log in.
#         if not self.creds or not self.creds.valid:

#             # If token is expired, it will be refreshed,
#             # else, we will request a new one.
#             if self.creds and self.creds.expired and self.creds.refresh_token:
#                 self.creds.refresh(Request())
#             else:
#                 flow = InstalledAppFlow.from_client_secrets_file(
#                     "src/common/credentials.json", SCOPES
#                 )
#                 self.creds = flow.run_local_server(port=0)

#             # Save the access token in token.pickle
#             # file for future usage
#             with open("token.pickle", "wb") as token:
#                 pickle.dump(self.creds, token)

#         # Connect to the API service
#         self.service = build("drive", "v3", credentials=self.creds)

#     def listFolders(self):
#         try:
#             page_token = None
#             folders = []
#             while True:
#                 response = (
#                     self.service.files()
#                     .list(
#                         q="mimeType='application/vnd.google-apps.folder'",
#                         spaces="drive",
#                         fields="nextPageToken, files(id, name)",
#                         pageToken=page_token,
#                     )
#                     .execute()
#                 )

#                 for file in response.get("files", []):
#                     # Process change
#                     folder_data = (file.get("name"), file.get("id"))
#                     folders.append(folder_data)

#                 page_token = response.get("nextPageToken", None)
#                 if page_token is None:
#                     break

#             return folders
#         except Exception as e:
#             print(str(e))
#             return None
        


# class Uploader(DriveAPI):
#     def __init__(self):
#         super(Uploader, self).__init__()

#     def createFolder(self, folder_name, parent_folder_id=None):
#         file_metadata = {
#             'name': folder_name,
#             'mimeType': 'application/vnd.google-apps.folder'
#         }
#         if parent_folder_id:
#             file_metadata['parents'] = [parent_folder_id]

#         folder = self.service.files().create(body=file_metadata, fields='id').execute()
#         return folder.get('id')

#     def uploadFile(self, file_path, parent_folder_id=None):
#         file_metadata = {'name': os.path.basename(file_path)}
#         if parent_folder_id:
#             file_metadata['parents'] = [parent_folder_id]

#         media = MediaFileUpload(file_path, resumable=True)
#         file = self.service.files().create(body=file_metadata, media_body=media, fields='id').execute()
#         return file.get('id')

#     def uploadFolder(self, folder_path, parent_folder_id=None, new_folder_name=None):
#         # Use the new_folder_name if provided, otherwise use the local folder name
#         folder_name = new_folder_name if new_folder_name else os.path.basename(folder_path)
#         folder_id = self.createFolder(folder_name, parent_folder_id)
#         for item in os.listdir(folder_path):
#             item_path = os.path.join(folder_path, item)
#             if os.path.isdir(item_path):
#                 self.uploadFolder(item_path, folder_id)
#             else:
#                 self.uploadFile(item_path, folder_id)
#         return folder_id