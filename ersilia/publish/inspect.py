from .. import ErsiliaBase
import requests
import subprocess
import json
from urllib.request import urlopen
#from ..hub.content.card import RepoMetadataFile
#from ..hub.content.card import ReadmeMetadata

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

        # test = RepoMetadataFile(self.model)
        # print(test)
        # test2 = ReadmeMetadata(self.model)
        # print(test2)

        if file is not None:
            try:
                if file['Publication'] and file['Source Code'] and file['S3'] and file['DockerHub']: # Parse through json object and ensure 
                    # pub_url_works = requests.head(file['Publication']).status_code == 200
                    pub_url_works = requests.head(file['Publication']).status_code != 404
                    print("URL: ", file['Publication'])
                    print("Works? ", pub_url_works)
                    
                    source_url_works = requests.head(file['Source Code']).status_code == 200
                    print("URL: ", file['Source Code'])
                    print("Works? ", source_url_works)

                    s3_url_works = requests.head(file['S3']).status_code == 200
                    print("URL: ", file['S3'])
                    print("Works? ", s3_url_works)

                    docker_url_works = requests.head(file['DockerHub']).status_code == 200
                    print("URL: ", file['DockerHub'])
                    print("Works? ", docker_url_works)

                    # Other idea print("socket", socket.gethostbyname(file['S3']))
                    if(not (pub_url_works and source_url_works and s3_url_works and docker_url_works)):
                        print("All links do not work")
                        return False
                else:
                    print("All metadata links not provided")
                    return False
            except (KeyError): # If a given key not present in json file return false
                print("All metadata categories not provided")
                return False
        return True # Otherwise, if the key was present but has no value return false
    
    def folderStructureComplete(self):
       # Validate folder structure of repository
        if requests.head(f"https://github.com/ersilia-os/{self.model}").status_code != 200: # Make sure repo exists
           return False
        url = f"https://github.com/ersilia-os/{self.model}"
        folders = [".github/workflows", "model", "src", "model/checkpoints", "model/framework"]
        for name in folders:
            response = requests.get(url + "/tree/main/" + name) # Check if the folders are present in a given repository
            if response.status_code != 200: 
                print(f"Folder {name} not found")
                return False # If the folder URL is not valid return false
            
        files = ["LICENSE", "Dockerfile"]
        for name in files:
            response = requests.get(url + "/blob/main/" + name) # Check if the files are present in a given repository
            if response.status_code != 200: 
                print(f"File {name} not found")
                return False # If the folder URL is not valid return false
        return True

    def validateDependicies(self):
        if requests.head(f"https://github.com/ersilia-os/{self.model}").status_code != 200: # Make sure repo exists
           return False
        url = f"https://raw.githubusercontent.com/ersilia-os/{self.model}/main/Dockerfile" # Get raw file from GitHub
        response = requests.get(url)
        file = response.text
        lines = file.split("\n")
        lines = [s for s in lines if s]
        for line in lines:
            if line.startswith('RUN pip install') and "rdkit" not in line:
                info = line.split('==')
                if len(info) < 2:
                    print(f"No specification found for {info[0]}.")
                    return False
                else:
                    specification = info[1]
                    if specification.strip()=="":
                        print(f"No specification found for {info[0]}.")
                        return False

        if "WORKDIR /repo" not in lines[len(lines) - 2]:
            print("Dockerfile is missing 'WORKDIR /repo' in the right place")
            return False

        if "COPY . /repo" not in lines[len(lines) - 1] and "COPY ./repo" not in lines[len(lines) - 1]:
            print("Dockerfile is missing 'COPY . /repo' in the right place or has incorrect syntax")
            return False
        return True
            