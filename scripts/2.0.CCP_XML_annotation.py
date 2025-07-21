import pandas as pd
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
from pathlib import Path

# Get the project's base directory
BASE_DIR = Path(__file__).parent.parent

CSV_PATH = BASE_DIR / "data" / "CCP" / "2021-09-ccp-corpus-toc.csv"
TEXT_DIR = BASE_DIR / "data" / "CCP"
OUTPUT_FILE = BASE_DIR / "data" / "CCP_annotated" / "AnnotatedCorpus1.xml"

# Load CSV file
try:
    df = pd.read_csv(CSV_PATH, dtype=str)
except FileNotFoundError:
    print(f"Error: File not found: {CSV_PATH}")
    print("Please make sure the CSV file is in the 'data' folder")
    exit(1)


def create_corpus():
    """Creates the XML corpus from text files and metadata."""
    root = ET.Element("corpus")
    
    for _, row in df.iterrows():
        doc = ET.SubElement(root, "document", id=row["docID"])
        
    #creating node with metadata from the csv file
        meta = ET.SubElement(doc, "meta")
        for field in ["eventID", "Convention_Type", "docTitle", "City", 
                     "State", "Country", "Item_Number", "URL"]:
            ET.SubElement(meta, field).text = row[field]
        
        # Process text file
        text_file = TEXT_DIR / f"{row['docID']}.txt"
        text_element = ET.SubElement(doc, "text")
        
        if text_file.exists():
            try:
                text_content = text_file.read_text(encoding="utf-8")
                text_element.text = text_content
            except Exception as e:
                print(f"Error loading {text_file}: {e}")
                text_element.text = "Error loading transcription"
        else:
            text_element.text = "No transcript available"
    
    return root

def save_xml(xml_root, output_file):
    """Saves the formatted XML to a file."""
    xml_str = ET.tostring(xml_root, encoding="utf-8")
    parsed_xml = minidom.parseString(xml_str)
    pretty_xml = parsed_xml.toprettyxml(indent="  ")
    
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(pretty_xml)
        print(f"XML file successfully generated: {output_file}")
    except Exception as e:
        print(f"Error saving XML file: {e}")

if __name__ == "__main__":
    # Create directory structure if it doesn't exist
    os.makedirs(OUTPUT_FILE.parent, exist_ok=True)
    
    # Generate the corpus
    corpus_root = create_corpus()
    
    # Save the XML file
    save_xml(corpus_root, OUTPUT_FILE)
