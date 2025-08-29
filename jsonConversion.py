import json
import argparse
import os

# Updated JSON schema to match your desired output structure
example_schema = {
    "type": "object",
    "patternProperties": {
        "^.*$": {
            "type": "object",
            "properties": {
                "Function": {"type": "string"},
                "Reference": {"type": "string"},
                "EntityType": {"type": "string"},
                "ApplicabilityCriteria": {
                    "type": "array",
                    "items": {"type": "string"}
                },
                "Type": {"type": "string"},
                "ValidationCriteria": {
                    "type": "object",
                    "properties": {
                        "MustSatisfy": {"type": "string"},
                        "Keyword": {"type": "string"},
                        "Requirement": {"type": "string"},
                        "Condition": {"type": "string"},
                        "Dependencies": {"type": "array", "items": {"type": "string"}}
                    },
                    "additionalProperties": True
                },
                "CRVersionIntroduced": {"type": "string"},
                "Status": {"type": "string"},
                "Notes": {"type": "string"}
            },
            "additionalProperties": True
        }
    }
}

def markdown_table_to_nested_json(markdown_string):
    """
    Converts a Markdown table into a single JSON object where each entry
    is a CRID, with the value containing the rest of the row's data. 
    This version correctly handles and preserves empty columns.

    Args:
        markdown_string (str): The input Markdown table string. 

    Returns:
        dict: A dictionary representing the table data. 
    """

    lines = markdown_string.strip().splitlines()

    # Find the header line (the one with | CRID | ...)
    header_line = next((line for line in lines if line.strip().startswith('| CRID')), None)
    if not header_line:
        print("Error: Could not find header line starting with '| CRID'.")
        return {}

    headers = [h.strip() for h in header_line.split('|') if h.strip()]
    header_indices = {h: i for i, h in enumerate(headers)}

    # Find all data lines: lines that start with '|' and have a non-empty CRID field
    data_lines = [
        line for line in lines
        if line.strip().startswith('|')
           and not line.strip().startswith('| CRID')
           and not set(line.strip()).issubset({'|', '-'})  # skip separator lines
           and line.split('|')[1].strip()                  # CRID field is not empty
           and not all(c == '-' for c in line.split('|')[1].strip())  # skip dashed CRID
    ]

    result = {}

    for line in data_lines:
        values = [v.strip() for v in line.split('|')[1:-1]]
        if len(values) < len(headers):
            values += [''] * (len(headers) - len(values))

        crid = values[header_indices['CRID']]

        # Build ValidationCriteria dictionary
        validation_criteria = {
            "MustSatisfy": values[header_indices.get('MustSatisfy', '')],
            "Keyword": values[header_indices.get('Keyword', '')],
            "Requirement": values[header_indices.get('Requirement', '')],
            "Condition": values[header_indices.get('Condition', '')],
            "Dependencies": []  # You can parse dependencies from Requirement if needed
        }

        # Build ApplicabilityCriteria as a list
        applicability = [values[header_indices.get('ApplicabilityCriteria', '')]] if values[header_indices.get('ApplicabilityCriteria', '')] else []

        # Build the output dictionary for this CRID
        result[crid] = {
            "Function": values[header_indices.get('Function', '')],
            "Reference": values[header_indices.get('Reference', '')],
            "EntityType": "Column",
            "ApplicabilityCriteria": applicability,
            "Type": values[header_indices.get('Type', '')].capitalize(),
            "ValidationCriteria": validation_criteria,
            "CRVersionIntroduced": values[header_indices.get('CRVersionIntroduced', '')],
            "Status": values[header_indices.get('Status', '')].capitalize(),
            "Notes": values[header_indices.get('Notes', '')]
        }

    return result

def save_json_output(data, output_filename, output_dir='jsonoutput'):
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def process_all_md_files(input_dir, output_dir='jsonoutput'):
    for filename in os.listdir(input_dir):
        if filename.endswith('.md'):
            input_path = os.path.join(input_dir, filename)
            with open(input_path, 'r', encoding='utf-8') as f:
                markdown_string = f.read()
            json_data = markdown_table_to_nested_json(markdown_string)
            base_name = os.path.splitext(filename)[0]
            if base_name.endswith('_cr'):
                base_name = base_name[:-3]
            output_filename = base_name + '.json'
            if validate_json(json_data, example_schema):
                save_json_output(json_data, output_filename, output_dir)
            else:
                print(f"Validation failed for {filename}, not saving output.")

def validate_json(data, schema):
    try:
        jsonschema.validate(instance=data, schema=schema)
        print("JSON data is valid against the schema.")
        return True
    except jsonschema.ValidationError as e:
        print(f"JSON validation error: {e.message}")
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown table files in a directory to JSON files.")
    parser.add_argument("input_path", help="Path to the input Markdown file or directory.")
    args = parser.parse_args()

    input_path = args.input_path

    if os.path.isdir(input_path):
        process_all_md_files(input_path)
    elif os.path.isfile(input_path):
        with open(input_path, 'r', encoding='utf-8') as f:
            markdown_content = f.read()
        json_data = markdown_table_to_nested_json(markdown_content)
        base_name = os.path.splitext(os.path.basename(input_path))[0]
        if base_name.endswith('_cr'):
            base_name = base_name[:-3]
        output_filename = base_name + '.json'
        if validate_json(json_data, example_schema):
            save_json_output(json_data, output_filename)
            print(f"JSON output successfully written to 'jsonoutput/{output_filename}'.")
        else:
            print("Validation failed, output not saved.")
    else:
        print(f"Error: '{input_path}' is not a valid file or directory.")