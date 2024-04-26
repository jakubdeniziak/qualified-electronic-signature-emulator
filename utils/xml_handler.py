import xml.etree.ElementTree as ElementTree


def create_xml(tags):
    signature = ElementTree.Element("Signature")
    for tag, value in tags.items():
        ElementTree.SubElement(signature, tag).text = str(value)
    xml_str = ElementTree.tostring(signature, encoding='unicode', method='xml')
    return xml_str
