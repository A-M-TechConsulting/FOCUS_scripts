import json
import argparse
import os

def markdown_table_to_json(markdown_string):
    """Converts a markdown table string into a JSON array of objects. 
    
    Args:
        markdown_string (str): The input Markdown table string.
        
        Returns:
            str: A JSON formatted string representing the table data.
            """
    
    lines = markdown_string.strip().split('\n')

    if len(lines) < 2:
        return json.dumps([]) #Return empty array if no data rows
    
    # Extract headers from the first line
    headers = [h.strip() for h in lines[0].split('|') if h.strip()]

    # Skip the separator line (second line)
    data_lines = lines[2:]

    result = []
    for line in data_lines:
        values = [v.strip() for v in line.split('|') if v.strip()]
        if len(values) == len(headers):
            row_dict = {}
            for i, header in enumerate(headers):
                row_dict[header] = values[i]
            result.append(row_dict)

    return json.dumps(result, indent=4)  

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert a Markdown table file to JSON.")     
    parser.add_argument("input_file", help="Path to the input Markdown file.")
    parser.add_argument("-o", "--output_file", help="Path to the output JSON file (optional).")
    args = parser.parse_args()

    input_file_path = args.input_file
    output_file_path = args.output_file

    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' not found.")
    else:
        try:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            json_output = markdown_table_to_json(markdown_content)

            if output_file_path:
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(json_output)
                print(f"JSON output succesfully written to '{output_file_path}'.")       
            else:
                print(json_output)

        except Exception as e:
            print(f"An error occurred: {e}")                 


'''Future Enhancements
1. Command-Line Arguments ('argparse'):
2. File Reading and Error Handling:
3. JSON Output:

How to use this script:
Save the script: Save code as a Python file.
Create a Markdown table file.
Convert and print to console. <python script_name.py file_name.md>
Convert and save to JSON. <python script_name.py file_name.md -o output.json> 

'''