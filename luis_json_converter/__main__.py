# __main__.py
import sys
import argparse
import logging
from pathlib import Path
from luis_json_converter.converter import process_luis_model

def setup_logging() -> None:
    """
    Sets up the basic configuration for logging.
    
    Logs will be output to the console with the format including the timestamp, log level, and message.
    """
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_arguments() -> argparse.Namespace:
    """
    Parses command-line arguments using argparse.

    Returns:
        argparse.Namespace: Parsed command-line arguments.
    """
    parser = argparse.ArgumentParser(description='Process Azure LUIS model JSON files.')
    parser.add_argument('input_file', type=str, help='Path to the input LUIS JSON file')
    parser.add_argument('-o', '--output_dir', type=str, default='output', help="Directory to save the processed JSON file. Defaults to ./output'")
    return parser.parse_args()

def validate_input_file(input_file: str) -> Path:
    """
    Validates the input file path.

    Args:
        input_file (str): Path to the input file as a string.

    Returns:
        Path: Validated Path object for the input file.

    Raises:
        SystemExit: If the input file is not valid.
    """
    input_path = Path(input_file)
    if not input_path.is_file():
        logging.error(f"Error: {input_path} is not a valid file.")
        sys.exit(1)
    return input_path

def create_output_dir(output_dir: str) -> Path:
    """
    Creates the output directory if it does not exist.

    Args:
        output_dir (str): Path to the output directory as a string.

    Returns:
        Path: Path object for the output directory.
    """
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    return output_path

def main() -> None:
    """
    Main function to process the Azure LUIS model JSON file.

    This function sets up logging, parses command-line arguments, validates the input file,
    creates the output directory, and processes the LUIS model JSON file.
    """
    setup_logging()
    args = parse_arguments()
    
    input_path = validate_input_file(args.input_file)
    output_path = create_output_dir(args.output_dir)
    
    output_file = output_path / f"{input_path.stem}_clu{input_path.suffix}"
    
    try:
        process_luis_model(input_path, output_file)
        logging.info(f"Processed file saved to {output_file}")
    except Exception as e:
        logging.error(f"An error occurred while processing the file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
