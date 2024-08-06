import re
import json
import logging
from pathlib import Path
from typing import Any, Dict, List


class Converter:
    """
    Processes an Azure LUIS model JSON file to remove concatenated parent names from child entity names,
    handling special cases, and fixing character encoding issues.

    Attributes:
        luis_model (Dict[str, Any]): The original LUIS model JSON data.
        clu_model (Dict[str, Any]): The modified CLU model JSON data.
        mapping (Dict[str, str]): A dictionary mapping original entity names to their flattened names.
    """

    special_cases = {
        "WhereOperatorSubstractionExact": "SubstractionExact",
        "WhereOperatorSubstractionRange": "SubstractionRange",
        "WhereOperatorSumExact": "SumExact",
        "WhereOperatorSumRange": "SumRange",
        "WhereOperatorNumber": "Number",
    }

    def __init__(self, input_path: Path, output_path: Path):
        """
        Initializes the Converter with the given input and output file paths.

        Args:
            input_path (Path): Path to the input JSON file.
            output_path (Path): Path to the output JSON file.
        """
        self.input_path = input_path
        self.output_path = output_path
        self.luis_model: Dict[str, Any]
        self.clu_model: Dict[str, Any] = {}
        self.mapping: Dict[str, str] = {}
        self.logger = logging.getLogger(__name__)

    def convert(self) -> bool:
        """
        Converts the LUIS model JSON to a CLU-compatible JSON by flattening entity names,
        updating utterances, and handling special renaming cases. This method orchestrates
        the entire conversion process by reading the input JSON, renaming entities,
        updating utterances, and writing the output JSON. It logs the progress and any errors
        encountered during the conversion.

        Returns:
            bool: True if the conversion is successful, False if an error occurs.
        """
        try:
            self._read_luis_json()
            self._rename_entities()
            self._update_utterances()
            self._write_clu_json()
        except Exception as e:
            self.logger.error("Conversion FAILED! %s", e)
            return False
        return True

    def _read_luis_json(self) -> None:
        """
        Reads a JSON file and returns its content as a dictionary.

        Args:
            file_path (Path): The path to the JSON file.

        Returns:
            Dict[str, Any]: The content of the JSON file.
        """
        # Read and fix encoding of the JSON content
        self.logger.info(f"Reading JSON file from {self.input_path}")
        content = self.input_path.open().read().encode("windows-1252", errors="ignore").decode("utf-8", errors="ignore")
        self.luis_model = json.loads(content)

    def _write_clu_json(self) -> None:
        """
        Save the processed JSON content to the output file
        """
        self.logger.info(f"Saving modified CLU model to {self.output_path}")
        with self.output_path.open("w", encoding="utf-8") as f:
            json.dump(self.clu_model, f, indent=2)

    def _rename_entities(self) -> Dict[str, str]:
        """
        Rename the entity names by removing the parent's name from the entity name
        and returns a mapping of original names to new names.

        Returns:
            Dict[str, str]: A dictionary mapping original entity names to new names.
        """
        self.logger.info("Renaming entities")
        self.clu_model = self.luis_model.copy()
        if "entities" in self.luis_model:
            self.clu_model["entities"] = []
            for entity in self.luis_model["entities"]:
                new_entity = entity.copy()
                self._process_entity(new_entity, new_entity["name"])
                self.clu_model["entities"].append(new_entity)
        return self.mapping

    def _process_entity(self, entity: Dict[str, Any], parent_names: str = "") -> None:
        """
        Recursively processes an entity and its children to remove concatenated parent names from the children's names.

        Args:
            entity (Dict[str, Any]): The entity to process, containing potential child entities.
            parent_names (str): Concatenated names of all parents up to the current entity.
        """
        if "children" in entity:
            for child in entity["children"]:
                original_name = child["name"]
                if original_name in self.special_cases:
                    child["name"] = self.special_cases[original_name]
                else:
                    if parent_names:
                        pattern = f"^{parent_names}"
                        child["name"] = re.sub(pattern, "", original_name)

                if original_name != child["name"]:
                    self.mapping[original_name] = child["name"]

                new_parent_names = f"{parent_names}{child['name']}"
                self._process_entity(child, new_parent_names)

    def _update_utterances(self) -> None:
        """
        Updates the utterances in the CLU model to reflect the flattened entity names.
        """
        self.logger.info("Updating utterances")
        if "utterances" in self.luis_model:
            self.clu_model["utterances"] = []
            for utterance in self.luis_model["utterances"]:
                new_utterance = utterance.copy()
                self._update_entities_in_utterance(new_utterance["entities"])
                self.clu_model["utterances"].append(new_utterance)

    def _update_entities_in_utterance(self, entities: List[Dict[str, Any]]) -> None:
        """
        Recursively updates the entities in an utterance using the mapping.

        Args:
            entities (List[Dict[str, Any]]): The list of entities in an utterance.
        """
        for entity in entities:
            original_name = entity["entity"]
            if original_name in self.mapping:
                entity["entity"] = self.mapping[original_name]
            if "children" in entity:
                self._update_entities_in_utterance(entity["children"])
