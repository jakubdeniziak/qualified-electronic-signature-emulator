import xml.etree.ElementTree as ElementTree
from xml.dom import minidom


def create_xml(tags):
    signature = ElementTree.Element('Signature')
    for tag, value in tags.items():
        ElementTree.SubElement(signature, tag).text = str(value)
    xml_str = ElementTree.tostring(signature, encoding='unicode', method='xml')
    pretty_xml = minidom.parseString(xml_str).toprettyxml(indent='\t')
    return pretty_xml


def parse_xml(xml_string):
    root = ElementTree.fromstring(xml_string)
    data_dict = {}
    for child in root:
        data_dict[child.tag] = child.text
    return data_dict
