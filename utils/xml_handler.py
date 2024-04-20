import xml.etree.ElementTree as ElementTree


def data_to_xml_dictionary(data):
    xml_data = {
        "FileSize": data['file_size'],
        "FileExtension": data['file_extension'],
        "ModificationDate": data['modification_date'],
        "DocumentHash": data['document_hash'],
        "UserInfo": data['user_info'],
        "Timestamp": data['timestamp']
    }
    return xml_data


def create_xml(tags):
    signature = ElementTree.Element("Signature")
    for tag, value in tags.items():
        ElementTree.SubElement(signature, tag).text = str(value)
    xml_str = ElementTree.tostring(signature, encoding='unicode', method='xml')
    return xml_str
