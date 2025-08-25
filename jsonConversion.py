import json
import argparse
import os

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

    #Adjust for 0-based indexing: line 6 is index 5, line 8 is index 7
    header_line_index = 5  # Change if your header is at a different line
    data_start_line_index = header_line_index + 2  # Usually header + separator

    if len(lines) < data_start_line_index + 1:
        print("Warning: Markdown content is too short to contain a table at the specifiied lines.")
        return {}
    
    # Extract headers from the specified line
    try:
        header_line = lines[header_line_index]
        # Splitting headers, without striping empty strings only empty spaces. 
        headers = [h.strip() for h in header_line.split('|')]
        # Filter out the empty entries from the start and end of the split
        headers = [h for h in headers if h]
    except IndexError:
        print(f"Error: Could not find header line at index {header_line_index}.")
        return {}

    # Ensure CRID column exists
    #if 'CRID' not in headers:
       # print("Error: The Markdown table must contain a 'CRID' column.")
       # return []
    
    crid_index = headers.index('CRID')

    #Check for "CRID" column and get its index if it exists
    crid_index = headers.index('CRID') if 'CRID' in headers else -1
    if crid_index == -1:
        print("Warning: 'CRID' column not found. The resulting JSON will not include a crid attribute.")

    # Data starts from data_start_line_index
    data_lines = lines[data_start_line_index:]

    # Initialize a dict to store all row objects by CRID
    final_json_data = {}

    for i, line in enumerate(data_lines):
        values = [v.strip() for v in line.split('|')]
        if values and values[0] == '':
            values = values[1:]
        if values and values[-1] == '':
            values = values[:-1]

        # Pad values to match headers length
        if len(values) < len(headers):
            values += [''] * (len(headers) - len(values))

        crid = values[crid_index]
        if crid:
            row_entry = {}
            for j, header in enumerate(headers):
                if header != 'CRID':
                    row_entry[header] = values[j]
            final_json_data[crid] = row_entry

    return final_json_data

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert Markdown table file into a JSON file based on CRIDs.")
    parser.add_argument("input_file", help="Path to the input Markdown file.")
    parser.add_argument("-o","--output_file", help="Path to the output JSON file.")
    args = parser.parse_args()

    input_file_path = args.input_file
    output_file_path = args.output_file

    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' not found.")
    else:
        try:
            with open(input_file_path, 'r', encoding='utf-8') as f:
                markdown_content = f.read()

            json_data = markdown_table_to_nested_json(markdown_content)

            with open(output_file_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=4)
            print(f"JSON output successfully written to '{output_file_path}'.")

        except Exception as e:
            print(f"An error occurred: {e}")