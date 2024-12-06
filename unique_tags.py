import sys
import xml.etree.ElementTree as ET

def extract_unique_tags(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    tags = set()

    for elem in root.iter():
        tags.add(elem.tag)

    return list(tags)

def write_tags_to_file(tags, output_file):
    with open(output_file, 'w') as f:
        f.write("all_tags = [\n")
        for tag in tags:
            f.write(f"    '{tag}'\n")
        f.write("]\n")

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print("Usage: python unique_tags.py <input_xml_file> <output_file>")
        sys.exit(1)

    input_xml_file = sys.argv[1]
    output_file = sys.argv[2]

    tags = extract_unique_tags(input_xml_file)
    write_tags_to_file(tags, output_file)
    print(f"Unique tags written to {output_file}")
