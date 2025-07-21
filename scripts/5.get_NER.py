import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

xml_file = BASE_DIR / "data" / "CCP_annotated" / "CCP_annotatedSpacy.xml"  #CCP_annotated/MLK_annotated.xml 
tree = ET.parse(xml_file)
root = tree.getroot()

#function to extract named entities (NER) from the XML excluding numbers and locations
def extract_entities_from_xml(root):
    entities = []
    excluded_labels = {"CARDINAL", "GPE"}  #exclude labels corresponding to numbers (CARDINAL) and locations (GPE)
    for entity in root.iter("entity"):
        label = entity.attrib.get("label", "")
        text = entity.text.strip() if entity.text else ""
        
        if label and text and label not in excluded_labels:  
            entities.append((label, text))  
    return entities

#extract entities from the XML
entities = extract_entities_from_xml(root)

#count how many times each entity appears (considering only the entity text)
entity_counter = Counter([entity[1] for entity in entities])

#retrieve the 20 most frequently mentioned entities
most_common_entities = entity_counter.most_common(20)
print("The 20 most frequently mentioned entities (excluding numbers and locations):")
for entity, count in most_common_entities:
    print(f"{entity}: {count} times")
