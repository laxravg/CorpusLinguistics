import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent

xml_file = BASE_DIR / "data" / "CCP_annotated" / "CCP_annotatedSpacy.xml"  #CCP_annotated/MLK_annotated.xml 
tree = ET.parse(xml_file)
root = tree.getroot()

#extracting the tokens
def extract_tokens_from_xml(root):
    tokens = []
    for token in root.iter("token"):

        text = token.text.strip() if token.text else ""
        pos = token.attrib.get("pos", "")
        lemma = token.attrib.get("lemma", "")
        tokens.append({"text": text, "pos": pos, "lemma": lemma})
    return tokens


tokens = extract_tokens_from_xml(root)

#converting the tokens to text
text = " ".join([token["text"] for token in tokens])

#dividing the text in chunks to be able to process it
chunk_size = 100000
chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]

#counting the words to get bi-grams
bigram_counter = Counter()


for idx, chunk in enumerate(chunks):
    print(f"Processing chunk {idx+1}/{len(chunks)}...")
    

    tokens_in_chunk = chunk.split()
    

    for token1, token2 in zip(tokens_in_chunk[:-1], tokens_in_chunk[1:]):
        #extraction of bigrams
        bigram = (token1, token2)
        bigram_counter[bigram] += 1  

#getting the 20 most frequent bigrams.
most_common_bigrams = bigram_counter.most_common(20)
print("20 most frequent bigrams:")
for bigram, count in most_common_bigrams:
    print(f"{bigram[0]} {bigram[1]}: {count} times")

