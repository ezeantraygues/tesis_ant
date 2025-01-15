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

class Downloader(DriveAPI):
    def __init__(self, vervose=False):
        super(Downloader, self).__init__()
        self.DEFAULT_STORAGE_PATH = "drive_content"
        self.vervose = vervose

    def __create_Directory(self, path=None):
        if path is None:
            path = self.DEFAULT_STORAGE_PATH
        if not os.path.isdir(path):
            os.mkdir(path=path)

        return path

    def getAllFiles(self, folderId, destinationFolder=None):
        path = self.__create_Directory(destinationFolder)
        page_token = None

        all_files = []

        while True:
            results = (
                self.service.files()
                .list(
                    spaces="drive",
                    pageToken=page_token,
                    q="'{0}' in parents".format(folderId),
                    fields="nextPageToken, files(id, name, mimeType)",
                )
                .execute()
            )

            items = results.get("files", [])
            for item in items:
                itemName = item["name"]
                itemId = item["id"]
                itemType = item["mimeType"]
                if self.vervose:
                    print("Found item: {0} with Type: {1}".format(itemName, itemType))
                filePath = os.path.join(path, itemName)

                if itemType == "application/vnd.google-apps.folder":
                    if self.vervose:
                        print("\nStepping into folder: {0}".format(filePath))
                    all_files.extend(
                        self.getAllFiles(itemId, filePath)
                    )  # Recursive call
                else:
                    print("Adding file: {0}".format(filePath))
                    all_files.append(
                        {"item_id": itemId, "file_path": filePath, "mimeType": itemType}
                    )

            page_token = results.get("nextPageToken", None)
            if page_token is None:
                break

        return all_files

    def downloadFolder(self, folderId, destinationFolder=None):
        all_files = self.getAllFiles(folderId, destinationFolder)

        download_processes = []
        for f in all_files:
            p = Process(
                target=self.downloadFile,
                args=[f["item_id"], f["file_path"], f["mimeType"]],
            )
            p.start()
            download_processes.append(p)

        for process in download_processes:
            process.join()

        print("All files downloaded!")

    def downloadFile(self, fileId, filePath, mimeType):
        # Note: The parent folders in filePath must exist
        print("\t -> Downloading file with id: {0} name: {1}".format(fileId, filePath))

        # Define exportable Google Docs MIME types
        exportable_mime_types = {
            "application/vnd.google-apps.document": "application/pdf",
            "application/vnd.google-apps.spreadsheet": "text/csv",
            "application/vnd.google-apps.presentation": "application/vnd.openxmlformats-officedocument.presentationml.presentation"
        }

        if mimeType in exportable_mime_types:
            request = self.service.files().export_media(
                fileId=fileId, mimeType=exportable_mime_types[mimeType]
            )
            file_extension = exportable_mime_types[mimeType].split("/")[-1]
            filePath = filePath + f".{file_extension}"
        else:
            request = self.service.files().get_media(fileId=fileId)

        fh = io.FileIO(filePath, mode="wb")

        try:
            downloader = MediaIoBaseDownload(fh, request, chunksize=1024 * 1024)
            current_progress = -1
            done = False
            while not done:
                status, done = downloader.next_chunk(num_retries=2)
                if status:
                    progress = int(status.progress() * 100)
                    if progress % 10 == 0 and progress != current_progress:
                        print(
                            " \t Downloading fileId: {0}, {1}% complete!".format(
                                fileId, int(status.progress() * 100)
                            )
                        )
                        current_progress = progress
            print("Download Complete!")
        except Exception as e:
            print(str(e))
            return
        finally:
            fh.close()

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
