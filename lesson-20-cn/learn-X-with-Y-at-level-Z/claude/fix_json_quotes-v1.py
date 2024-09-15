import json
import re

def fix_nested_quotes(json_string):
    # Step 1: Temporarily replace outer quotes of each string with a unique marker
    outer_quote_marker = "OUTER_QUOTE_MARKER"
    pattern = r'"([^"\\]*(?:\\.[^"\\]*)*)"'
    marked_json = re.sub(pattern, f'{outer_quote_marker}\\1{outer_quote_marker}', json_string)
    
    # Step 2: Replace remaining double quotes with escaped quotes
    marked_json = marked_json.replace('"', '\\"')
    
    # Step 3: Restore outer quotes
    fixed_json = marked_json.replace(outer_quote_marker, '"')
    
    return fixed_json

def process_json(input_json):
    # Fix nested quotes
    fixed_json_string = fix_nested_quotes(input_json)
    
    # Parse and re-serialize to ensure valid JSON and proper formatting
    try:
        parsed_json = json.loads(fixed_json_string)
        return json.dumps(parsed_json, ensure_ascii=False, indent=2)
    except json.JSONDecodeError as e:
        print(f"Error: Unable to parse JSON after fixing quotes. {str(e)}")
        return None

# Example usage
input_json = """YOUR_JSON_STRING_HERE"""  # Replace with your JSON string

output_json = process_json(input_json)

if output_json:
    print("Fixed JSON:")
    print(output_json)
    
    # Optionally, write to a file
    with open('fixed_json.json', 'w', encoding='utf-8') as f:
        f.write(output_json)
    print("Fixed JSON has been written to 'fixed_json.json'")
else:
    print("Failed to fix JSON.")