import json
import sys
import os
import pandas as pd

csv_headers = ["Subject", "Level", "Name", "Type", "Description", "URL", ]

def read_json(json_string):
    # Parse the JSON string
    try:
        parsed_json = json.loads(json_string)
        # If parsing succeeds, the JSON is valid. We'll re-serialize it to ensure proper formatting.
        return parsed_json
        # return json.dumps(parsed_json, ensure_ascii=False, indent=2)
    except json.JSONDecodeError as e:
        print(f"[ERROR] {str(e)}")
        return None

def write_file(output_file, data):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(data)

# def triple_quote(s):
#     return repr(s)
#     # return f'"""{s}"""'

def fix_value(val):
    return repr(val) if '"' in val or ',' in val or '\n' in val else val

# Function to flatten the JSON
def flatten_json(data):
    flattened = []
    for subject in data.keys():
        for level, resources in data[subject].items():
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

def process_json_file(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        json_content = file.read()
    
    parsed_json = read_json(json_content)
    
    if parsed_json is None or not parsed_json:
        print(f"[ERROR] Failed to process {input_file}")
        return

    # Flatten the JSON
    csv_content = flatten_json(parsed_json)
    df = pd.DataFrame(csv_content, columns=csv_headers)
    df.to_csv(output_file, index=False)
    # write_file(output_file, csv_content)
    print(f"Successfully processed {input_file} and saved to {output_file}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}.csv"
    
    process_json_file(input_file, output_file)

if __name__ == "__main__":
    main()