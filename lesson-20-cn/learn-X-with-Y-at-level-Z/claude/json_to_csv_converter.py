import json
import sys
import os
import pandas as pd
from typing import Dict, List, Any, Optional
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

csv_headers = ["Subject", "Level", "Name", "Type", "Description", "URL"]

def read_json(json_string: str) -> Optional[Dict[str, Any]]:
    try:
        return json.loads(json_string)
    except json.JSONDecodeError as e:
        logging.error(f"JSON Decode Error: {str(e)}")
        return None

def fix_value(val: str) -> str:
    return repr(val) if '"' in val or ',' in val or '\n' in val else val

def flatten_json(data: Dict[str, Any]) -> List[List[str]]:
    flattened = []
    for subject, levels in data.items():
        for level, resources in levels.items():
            for resource in resources:
                flattened.append([
                    subject,
                    level,
                    fix_value(resource.get("name", "")),
                    resource.get("type", ""),
                    fix_value(resource.get("description", "")),
                    resource.get("url", "")
                ])
    return flattened

def process_json_file(input_file: str, output_file: str) -> None:
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            json_content = file.read()
    except IOError as e:
        logging.error(f"Error reading input file: {str(e)}")
        return

    parsed_json = read_json(json_content)
    
    if parsed_json is None or not parsed_json:
        logging.error(f"Failed to process {input_file}")
        return

    csv_content = flatten_json(parsed_json)
    df = pd.DataFrame(csv_content, columns=csv_headers)
    
    try:
        df.to_csv(output_file, index=False)
        logging.info(f"Successfully processed {input_file} and saved to {output_file}")
    except IOError as e:
        logging.error(f"Error writing output file: {str(e)}")

def main() -> None:
    if len(sys.argv) < 2:
        logging.error("Usage: python script.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        base, _ = os.path.splitext(input_file)
        output_file = f"{base}.csv"
    
    process_json_file(input_file, output_file)

if __name__ == "__main__":
    main()