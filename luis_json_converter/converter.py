# migrator.py
import json
import re
from pathlib import Path
from typing import Any, Dict

# Dictionary for special cases to handle specific entity renaming
special_cases = {
    'WhereOperatorSubstractionExact': 'SubstractionExact',
    'WhereOperatorSubstractionRange': 'SubstractionRange',
    'WhereOperatorSumExact': 'SumExact',
    'WhereOperatorSumRange': 'SumRange',
    'WhereOperatorNumber': 'Number'
}

def process_entity(entity: Dict[str, Any], parent_names: str = "") -> None:
    """
    Recursively processes an entity and its children to remove concatenated parent names from the children's names.

    Args:
        entity (Dict[str, Any]): The entity to process, containing potential child entities.
        parent_names (str): Concatenated names of all parents up to the current entity.

    Returns:
        None
    """
    if 'children' in entity:
        for child in entity['children']:
            # Check if the child's name is in special_cases dictionary
            if child['name'] in special_cases:
                child['name'] = special_cases[child['name']]
            else:
                # Remove parent names from the beginning of the child's name if present
                if parent_names:
                    pattern = f"^{parent_names}"
                    child['name'] = re.sub(pattern, "", child['name'])
            # Update the parent names for the next level of recursion
            new_parent_names = f"{parent_names}{child['name']}"
            # Recursively process child entities
            process_entity(child, new_parent_names)

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
    
    # Process each entity in the 'entities' list
    if 'entities' in luis_model:
        for entity in luis_model['entities']:
            process_entity(entity, entity['name'])
    
    # Save the processed JSON content to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(luis_model, f, indent=2)
