from .. import ErsiliaBase
import requests
import json
from urllib.request import urlopen


class ModelInspector(ErsiliaBase):
    def __init__(self, model, config_json=None):
        ErsiliaBase.__init__(self, config_json=config_json, credentials_json=None)
        self.model = model


    def checkRepoExists(self):
        url = f"https://github.com/ersilia-os/{self.model}"
        response = requests.head(url)
        return response.status_code == 200
    
    def metadataComplete(self):
       # search for three words in metadata json file
        url = f"https://raw.githubusercontent.com/ersilia-os/{self.model}/main/metadata.json"
        response = requests.get(url)
        print(response.content)
        # data = json.loads(file.read())
        print(response, type(response))
        return "True"
        # r = file.json() 
        # metadata_dict = json.loads(file)
        # if metadata_dict is not None:
        #     if metadata_dict['Identifier'] and metadata_dict['Slug'] and metadata_dict['Status'] is not None:
        #         return True
