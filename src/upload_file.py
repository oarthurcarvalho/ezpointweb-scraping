import glob
from typing import Any, Dict, List

import msal
from decouple import config
from office365.graph_client import GraphClient


class SharepointUploader:

    """
    A class for uploading files to SharePoint using Microsoft Graph API.

    Attributes:
    - SITE_NAME (str): The name of the SharePoint site.
    - SHAREPOINT_HOST_NAME (str): The host name of the SharePoint server.
    - TENANT_ID (str): The ID of the Azure AD tenant.
    - CLIENT_ID (str): The client ID for authentication.
    - CLIENT_SECRET (str): The client secret for authentication.
    - UPLOAD_PATH (str): The path in SharePoint where files will be uploaded.
    - FILE_PATH (str): The local path where files to be uploaded are located.
    - tenant_url (str): The URL of the SharePoint site with the specified host
        and site name.
    - local_files (list): A list of local file paths to be uploaded.

    Methods:
    - acquire_token(): Acquires an authentication token using MSAL for
        Microsoft Graph API.
    - upload_file(): Uploads files from the local path to the specified
        SharePoint location.
    """

    def __init__(self) -> None:
        """
        Initializes the SharepointUploader with configuration values.
        """

        self.SITE_NAME: str = config('site_name')
        self.SHAREPOINT_HOST_NAME: str = config('sharepoint_host_name')
        self.TENANT_ID: str = config('tenant_id')
        self.CLIENT_ID: str = config('client_id')
        self.CLIENT_SECRET: str = config('client_secret')
        self.UPLOAD_PATH: str = config('upload_path')
        self.FILE_PATH: str = config('file_path')

        # below used with 'get_by_url' in GraphClient calls
        self.tenant_url: str = f'https://{self.SHAREPOINT_HOST_NAME}' \
            f'/sites/{self.SITE_NAME}'

        # we're running this in actions, so we'll only ever have one .md file
        self.local_files: List[str] = glob.glob(self.FILE_PATH)

    def acquire_token(self) -> Dict[str, Any]:
        """
        Acquires an authentication token for Microsoft Graph API using MSAL.

        Returns:
        - dict: The acquired authentication token.
        """
        authority_url = f'https://login.microsoftonline.com/{self.TENANT_ID}'
        app = msal.ConfidentialClientApplication(
            authority=authority_url,
            client_id=self.CLIENT_ID,
            client_credential=self.CLIENT_SECRET
        )
        token: Dict[str, Any] = app.acquire_token_for_client(
            scopes=["https://graph.microsoft.com/.default"])
        return token

    def upload_file(self) -> None:
        """
        Uploads files from the local path to the specified SharePoint location
        using Microsoft Graph API.

        Raises:
        - Exception: If an unexpected error occurs during the upload process.
        """
        client: GraphClient = GraphClient(self.acquire_token)
        drive = client.sites.get_by_url(
            self.tenant_url).drive.root.get_by_path(self.UPLOAD_PATH)

        for f in self.local_files:
            try:
                remote_file = drive.upload_file(f).execute_query()
                print(f"File {remote_file.web_url} has been uploaded")
            except Exception as e:
                print(f"Unexpected error occurred: {e}, {type(e)}")
