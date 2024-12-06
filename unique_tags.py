import sys
import xml.etree.ElementTree as ET

def extract_unique_tags(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    tags = set()
    tag_data = {}

    def recursive_tag_extraction(element, prefix):
        tag = element.tag
        if '}' in tag:
            tag = tag.split('}', 1)[1]
        current_tag = f"{prefix}_{tag}" if prefix else tag
        tags.add(current_tag)

        # Analyze the length and data type of the tag's text
        if element.text and element.text.strip():
            text_length = len(element.text.strip())
            data_type = 'VARCHAR'  # Default data type
            tag_data[current_tag] = (data_type, text_length)

        for child in element:
            recursive_tag_extraction(child, current_tag)

    for elem in root:
        recursive_tag_extraction(elem, '')

    return tags, tag_data

def generate_mysql_script(tags, tag_data):
    script_lines = ["USE botransactions;", "CREATE TABLE customers ("]

    for tag in sorted(tags):
        if tag in tag_data:
            data_type, text_length = tag_data[tag]
            column_definition = f"    {tag} {data_type}({text_length})"
        else:
            column_definition = f"    {tag} VARCHAR(255)"

        if tag == 'customer_id':
            column_definition += " PRIMARY KEY"

        script_lines.append(column_definition)

    script_lines.append(");")
    return "\n".join(script_lines)

def write_tags_to_file(tags, tag_data, output_file):
    mysql_script = generate_mysql_script(tags, tag_data)
    with open(output_file, 'w') as f:
        f.write(mysql_script)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python unique_tags.py <input_xml_file> <output_file>")
        sys.exit(1)

    input_xml_file = sys.argv[1]
    output_file = sys.argv[2]

    tags, tag_data = extract_unique_tags(input_xml_file)
    write_tags_to_file(tags, tag_data, output_file)
    print(f"MySQL script written to {output_file}")
