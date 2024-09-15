import json
import sys
import os

def fix_json_content(json_string):
    # Parse the JSON string
    try:
        parsed_json = json.loads(json_string)
        # If parsing succeeds, the JSON is valid. We'll re-serialize it to ensure proper formatting.
        return json.dumps(parsed_json, ensure_ascii=False, indent=2)
    except json.JSONDecodeError as e:
        # If parsing fails, we'll try to fix common issues
        print(f"Warning: Invalid JSON detected. Attempting to fix... Error: {str(e)}")
        
        # Replace smart quotes with straight quotes
        json_string = json_string.replace('"', '"').replace('"', '"')
        
        # Handle escaped quotes within string values
        json_string = json_string.replace('\\"', '"')
        
        # Try parsing again after fixes
        try:
            parsed_json = json.loads(json_string)
            return json.dumps(parsed_json, ensure_ascii=False, indent=2)
        except json.JSONDecodeError as e:
            print(f"Error: Unable to fix JSON. {str(e)}")
            return None

def write_file(output_file, data):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(data)

def process_json_file(input_file, output_file):
    try:
        with open(input_file, 'r', encoding='utf-8') as file:
            json_content = file.read()
        
        fixed_json_content = fix_json_content(json_content)
        
        if fixed_json_content:
            write_file(output_file, fixed_json_content)
            print(f"Successfully processed {input_file} and saved to {output_file}")
        else:
            print(f"Failed to process {input_file}")
    
    except IOError as e:
        print(f"Error: Unable to read or write file")
        print(f"Error message: {str(e)}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <input_file> [output_file]")
        sys.exit(1)
    
    input_file = sys.argv[1]
    
    if len(sys.argv) > 2:
        output_file = sys.argv[2]
    else:
        # Generate output filename by adding "-fixed" before the extension
        base, ext = os.path.splitext(input_file)
        output_file = f"{base}-fixed{ext}"
    
    process_json_file(input_file, output_file)

if __name__ == "__main__":
    main()