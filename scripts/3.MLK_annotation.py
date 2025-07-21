import spacy
from pathlib import Path
import xml.etree.ElementTree as ET

#identing the xml file
def indent(elem, level=0):
    
    i = "\n" + level * "  "
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + "  "
        for e in elem:
            indent(e, level + 1)
        if not e.tail or not e.tail.strip():
            e.tail = i
    if level and (not elem.tail or not elem.tail.strip()):
        elem.tail = i


nlp = spacy.load("en_core_web_sm")

#paths
BASE_DIR = Path(__file__).parent.parent

input_dir = BASE_DIR / "data" / "MLK"
output_dir = BASE_DIR / "data" / "MLK_annotated" 

output_dir.mkdir(parents=True, exist_ok=True)

root = ET.Element("corpus")

#adding the metadata according to the information from the book
metadata = {
    "01.txt": {"title": "Give Us the Ballot", "date": "1957-05-17", "place": "Washington, D.C."},
    "02.txt": {"title": "Loving Your Enemies", "date": "1957-11-17", "place": "Dexter Avenue Baptist Church, Montgomery, Alabama"},
    "03.txt": {"title": "Letter from Birmingham Jail", "date": "1963-04-16", "place": "Birmingham, Alabama"},
    "04.txt": {"title": "Lincoln Memorial Address", "date": "1963-08-28", "place": "Washington, D.C."},
    "05.txt": {"title": "I Have a Dream", "date": "1963-08-28", "place": "Lincoln Memorial, Washington, D.C."},
    "06.txt": {"title": "The Nobel Peace Prize Acceptance Speech", "date": "1964-12-10", "place": "Oslo, Norway"},
    "07.txt": {"title": "Our God Is Marching On", "date": "1965-03-25", "place": "Selma, Alabama"},
    "08.txt": {"title": "Beyond Vietnam", "date": "1967-04-04", "place": "New York, N.Y."},
    "09.txt": {"title": "The Three Dimensions of A Complete Life", "date": "1967-04-09", "place": "New Covenant Baptist Church, Chicago, Illinois"},
    "10.txt": {"title": "Where Do We Go From Here", "date": "1967-08-16", "place": "Southern Christian Leadership Conference, Atlanta, Georgia"},
    "11.txt": {"title": "I've Been to the Mountaintop", "date": "1968-04-03", "place": "Mason Temple, Memphis, Tennessee"}
}


for file_path in input_dir.glob("*.txt"):
    file_name = file_path.name

    if file_name not in metadata:
        print(f"No metadata for: {file_name}")
        continue

    text = file_path.read_text(encoding="utf-8")
    doc = nlp(text)


    document_el = ET.SubElement(root, "document", id=file_name)

    #metadata
    meta = ET.SubElement(document_el, "metadata")
    ET.SubElement(meta, "title").text = metadata[file_name]["title"]
    ET.SubElement(meta, "date").text = metadata[file_name]["date"]
    ET.SubElement(meta, "place").text = metadata[file_name]["place"]

    #content
    body = ET.SubElement(document_el, "body")

    for i, sent in enumerate(doc.sents):
        para_el = ET.SubElement(body, "paragraph", id=f"p{i+1}")

        tokens_el = ET.SubElement(para_el, "tokens")
        for token in sent:
            token_el = ET.SubElement(tokens_el, "token")
            token_el.set("pos", token.pos_)
            token_el.text = token.text  # El texto del token

    #entities
    entities_el = ET.SubElement(document_el, "entities")
    for ent in doc.ents:
        ent_el = ET.SubElement(entities_el, "entity")
        ent_el.set("label", ent.label_)
        ent_el.text = ent.text  # El texto de la entidad

    print(f"Anotado: {file_name}")

#saving the xml file
indent(root)
tree = ET.ElementTree(root)
output_file = output_dir / "MLK_annotated.xml"
tree.write(output_file, encoding="utf-8", xml_declaration=True)

print("All xml files have been annotated.")
