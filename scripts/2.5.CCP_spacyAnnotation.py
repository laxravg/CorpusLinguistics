import pandas as pd
import os
import spacy
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

def load_spacy_model():
    """Load the spaCy English language model."""
    try:
        return spacy.load("en_core_web_sm")
    except OSError:
        print("Downloading spaCy English model...")
        import subprocess
        subprocess.run(["python", "-m", "spacy", "download", "en_core_web_sm"])
        return spacy.load("en_core_web_sm")

# Get the project's base directory
BASE_DIR = Path(__file__).parent.parent

# Define paths
CSV_PATH = BASE_DIR / "data" / "CCP" / "2021-09-ccp-corpus-toc.csv"
TEXT_DIR = BASE_DIR / "data" / "CCP"
OUTPUT_DIR = BASE_DIR / "data" / "CCP_annotated"
OUTPUT_FILE = OUTPUT_DIR / "AnnotatedCorpusSpacy.xml"

def load_csv_data():
    """Load and return the CSV data."""
    try:
        return pd.read_csv(CSV_PATH, dtype=str)
    except FileNotFoundError:
        print(f"Error: File not found: {CSV_PATH}")
        print("Please make sure the CSV file exists in the specified location.")
        exit(1)

def process_text(text, doc_id):
    """Process text with spaCy and return the processed doc."""
    if text.strip() == "No transcript available":
        return None
    try:
        return nlp(text)
    except Exception as e:
        print(f"Error processing document {doc_id}: {e}")
        return None

def create_xml_structure(df):
    """Create the XML structure with spaCy annotations."""
    root = ET.Element("corpus")
    
    for _, row in df.iterrows():
        doc_id = row["docID"]
        doc_element = ET.SubElement(root, "document", id=doc_id)
        
        # Add metadata
        meta = ET.SubElement(doc_element, "meta")
        for field in ["eventID", "Convention_Type", "docTitle", "City", 
                     "State", "Country", "Item_Number", "URL"]:
            ET.SubElement(meta, field).text = row[field]
        
        # Process text file
        text_file = TEXT_DIR / f"{doc_id}.txt"
        text_content = text_file.read_text(encoding="utf-8") if text_file.exists() else "No transcript available"
        
        # Process with spaCy if text is available
        nlp_doc = process_text(text_content, doc_id)
        
        # Add annotated text
        annotated_text = ET.SubElement(doc_element, "annotated_text")
        if nlp_doc:
            for token in nlp_doc:
                ET.SubElement(annotated_text, "token", pos=token.pos_).text = token.text
        
        # Add named entities
        entities_element = ET.SubElement(doc_element, "named_entities")
        if nlp_doc and nlp_doc.ents:
            for ent in nlp_doc.ents:
                ET.SubElement(entities_element, "entity", label=ent.label_).text = ent.text
    
    return root

def save_xml(xml_root, output_file):
    """Save the XML structure to a file."""
    try:
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Convert to pretty XML
        xml_str = ET.tostring(xml_root, encoding="utf-8")
        parsed_xml = minidom.parseString(xml_str)
        pretty_xml = parsed_xml.toprettyxml(indent="  ")
        
        # Write to file
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(pretty_xml)
        
        print(f"XML successfully saved to: {output_file}")
        return True
    except Exception as e:
        print(f"Error saving XML file: {e}")
        return False

if __name__ == "__main__":
    # Load spaCy model
    nlp = load_spacy_model()
    
    # Load data
    df = load_csv_data()
    
    # Process and save
    xml_root = create_xml_structure(df)
    save_xml(xml_root, OUTPUT_FILE)
