import joblib
import openai
from pathlib import Path
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Base directory (project root)
BASE_DIR = Path(__file__).parent.parent

# Define folders relative to BASE_DIR
TOPICDOCS_DIR = BASE_DIR / 'output' / 'TopicDocs'
folders = {
    'MLK': TOPICDOCS_DIR / 'MLK',
    'CCP': TOPICDOCS_DIR / 'CCp'
}

# Output folder for images
output_base = TOPICDOCS_DIR / 'Wordclouds'

# Iterate through each folder
for folder_name, folder_path in folders.items():
    output_folder = output_base / folder_name
    output_folder.mkdir(parents=True, exist_ok=True)  # Create output folder if it doesn't exist

    for i, txt_file in enumerate(folder_path.glob('*.txt')):
        with txt_file.open('r', encoding='utf-8') as f:
            document = f.read()
        # Create the wordcloud
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate(document)
        # Save the image
        output_file = output_folder / f'{folder_name}_document_{i}.png'
        wordcloud.to_file(str(output_file))

print("All wordclouds have been saved'.")

