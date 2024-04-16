from ...publish.inspect import ModelInspector
import click
from . import ersilia_cli
import json


def inspect_cmd():

    @ersilia_cli.command(short_help="Serve model", help="Serve model")
    @click.argument("model", type=click.STRING)
    def inspect(model):

        inspector = ModelInspector(model)
        value = {
             'is_github_url_available': inspector.checkRepoExists(),
             'metadata_complete': inspector.metadataComplete(),
             'folder_structure_complete': inspector.folderStructureComplete(),
             'dependencies_valid': inspector.validateDependencies()
        }
        #print or return?
        print(json.dumps(value))
        return json.dumps(value)
    
    