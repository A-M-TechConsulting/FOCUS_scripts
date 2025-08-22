import json

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


# Example input and output:
markdown_table = """
| Header1 | Header2 | Header3 |
|---|---|---|
| Text1 | Text2 | Text3 |
| Text4 | Text5 | Text6 |
| Text7 | Text8 | Text9 |
"""

json_output = markdown_table_to_json(markdown_table)
print(json_output)