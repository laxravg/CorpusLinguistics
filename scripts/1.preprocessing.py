import os
import spacy
from pathlib import Path

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

def clean_text(text):
    """Clean text by removing stopwords and punctuation."""
    doc = nlp(text)
    clean_words = [token.text for token in doc if not token.is_stop and not token.is_punct]
    return ' '.join(clean_words)

def process_files():
    # Use relative path - will work from any location
    script_dir = Path(__file__).parent
    data_dir = script_dir.parent / 'data' 
    
    if not data_dir.exists():
        print("Error: 'data' directory not found next to 'scripts' folder")
        return
    
    processed_count = 0
    
    # Process all .txt files in data directory and its subdirectories
    for txt_file in data_dir.rglob('*.txt'):
        try:
            # Read the file
            with open(txt_file, 'r', encoding='utf-8') as f:
                text = f.read()
            
            # Clean the text
            cleaned_text = clean_text(text)
            
            # Overwrite the original file
            with open(txt_file, 'w', encoding='utf-8') as f:
                f.write(cleaned_text)
            
            processed_count += 1
            print(f" Processed: {txt_file.relative_to(script_dir.parent)}")
            
        except Exception as e:
            print(f" Error processing {txt_file.name}: {str(e)}")
    
    print(f"\nProcessing complete!")
    print(f"Processed {processed_count} files.")

if __name__ == "__main__":
    process_files()
