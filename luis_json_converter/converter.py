import re
import json
from pathlib import Path
from typing import Any, Dict

def process_luis_model(luis_json_file: Path, output_file: Path) -> None:
    """
    Processes an Azure LUIS model JSON file to remove concatenated parent names from child entity names,
    handling special cases, and fixing character encoding issues.

    Args:
        luis_json_file (Path): Path to the input LUIS model JSON file.
        output_file (Path): Path to the output file where the processed JSON will be saved.

    Returns:
        None
    """
    # Read and fix encoding of the JSON content
    content = (luis_json_file.open().read()
                        .encode('windows-1252', errors='ignore')
                        .decode('utf-8', errors='ignore'))
    
    # Load the JSON content into a Python dictionary
    luis_model = json.loads(content)

    converter = Converter(luis_model)
    mapping = converter.flatten_entities()

    # Save the processed JSON content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(converter.clu_model, f, indent=2)

class Converter:
    """
    A class to convert LUIS model JSON files to be compatible with Azure CLU by flattening entity names
    and handling special renaming cases.
    
    Attributes:
        luis_model (Dict[str, Any]): The original LUIS model JSON data.
        clu_model (Dict[str, Any]): The modified CLU model JSON data.
        mapping (Dict[str, str]): A dictionary mapping original entity names to their flattened names.
    """
        
    special_cases = {
        'WhereOperatorSubstractionExact': 'SubstractionExact',
        'WhereOperatorSubstractionRange': 'SubstractionRange',
        'WhereOperatorSumExact': 'SumExact',
        'WhereOperatorSumRange': 'SumRange',
        'WhereOperatorNumber': 'Number'
    }

    def __init__(self, luis_model: Dict[str, Any]):
        """
        Initializes the Converter with the given LUIS model.
        
        Args:
            luis_model (Dict[str, Any]): The original LUIS model JSON data.
        """
        self.luis_model = luis_model
        self.clu_model: Dict[str, Any] = {}
        self.mapping: Dict[str, str] = {}

    def flatten_entities(self) -> Dict[str, str]:
        """
        Flattens the entity names in the LUIS model and returns a mapping of original names to flattened names.
        
        Returns:
            Dict[str, str]: A dictionary mapping original entity names to flattened names.
        """
        self.clu_model = self.luis_model.copy()
        if 'entities' in self.luis_model:
            self.clu_model['entities'] = []
            for entity in self.luis_model['entities']:
                new_entity = entity.copy()
                self.process_entity(new_entity, new_entity['name'])
                self.clu_model['entities'].append(new_entity)
        return self.mapping

    def process_entity(self, entity: Dict[str, Any], parent_names: str = "") -> None:
        """
        Recursively processes an entity and its children to remove concatenated parent names from the children's names.
        
        Args:
            entity (Dict[str, Any]): The entity to process, containing potential child entities.
            parent_names (str): Concatenated names of all parents up to the current entity.
        """
        if 'children' in entity:
            for child in entity['children']:
                original_name = child['name']
                if original_name in self.special_cases:
                    child['name'] = self.special_cases[original_name]
                else:
                    if parent_names:
                        pattern = f"^{parent_names}"
                        child['name'] = re.sub(pattern, "", original_name)

                if original_name != child['name']:
                    self.mapping[original_name] = child['name']

                new_parent_names = f"{parent_names}{child['name']}"
                self.process_entity(child, new_parent_names)

    def update_utterances(self) -> None:
        # Placeholder for future implementation to update utterances
        pass
