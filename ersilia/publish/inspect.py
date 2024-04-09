from .. import ErsiliaBase
import requests
import json
from urllib.request import urlopen


class ModelInspector(ErsiliaBase):
    def __init__(self, model, config_json=None):
        ErsiliaBase.__init__(self, config_json=config_json, credentials_json=None)
        self.model = model


    def checkRepoExists(self): # Verify that repository exists at a given link
        url = f"https://github.com/ersilia-os/{self.model}"
        response = requests.head(url)
        return response.status_code == 200
    
    def metadataComplete(self):
       # Search for specific keys in metadata json file
        if requests.head(f"https://github.com/ersilia-os/{self.model}").status_code != 200: # Make sure repo exists
           return False
        url = f"https://raw.githubusercontent.com/ersilia-os/{self.model}/main/metadata.json" # Get raw file from GitHub
        response = requests.get(url)
        file = response.json() # Save as json object

        if file is not None:
            try:
                if file['Identifier'] and file['Slug'] and file['Status'] is not None: # Parse through json object and ensure 
                    return True
            except (KeyError): # If a given key not present in json file return false
                return False
        return False # Otherwise, if the key was present but has no value return false
    
    def folderStructureComplete(self):
       # Validate folder structure of repository
        if requests.head(f"https://github.com/ersilia-os/{self.model}").status_code != 200: # Make sure repo exists
           return False
        url = f"https://github.com/ersilia-os/{self.model}"
        folders = [".github/workflows", "model", "src", "model/checkpoints", "model/framework"]
        for name in folders:
            response = requests.get(url + "/tree/main/" + name) # Check if the folders are present in a given repository
            if response.status_code != 200: 
                return False # If the folder URL is not valid return false
        return True
