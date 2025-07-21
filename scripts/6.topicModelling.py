import os
import xml.etree.ElementTree as ET
from pathlib import Path
from bertopic import BERTopic
from umap import UMAP
import joblib


# Paths
BASE_DIR = Path(__file__).parent.parent
OUTPUT_DIR = BASE_DIR / "output"
DATA_DIR = BASE_DIR / "data"
TOPICS_MODEL_DIR = OUTPUT_DIR / "TopicsModel"
TOPIC_WORDS_DIR = OUTPUT_DIR / "TopicWords"


# Functions

def extract_tokens(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    tokens = []

    for token in root.findall('.//token'):
        word = token.text
        pos = token.attrib.get('pos')
        ner = None
        if word:
            tokens.append((word, pos, ner))

    for entity in root.findall('.//entity'):
        word = entity.text
        ner = entity.attrib.get('label')
        pos = None
        if word:
            tokens.append((word, pos, ner))

    return tokens


def filter_tokens(tokens):
    return [
        word.lower()
        for word, pos, ner in tokens
        if word and ((pos in ['NOUN', 'PROPN', 'ADJ']) or (ner in ['PERSON', 'ORG', 'LOC']))
    ]


def chunk_documents(tokens, chunk_size=100):
    docs = [" ".join(tokens[i:i + chunk_size]) for i in range(0, len(tokens), chunk_size)]
    return [doc for doc in docs if len(doc.strip()) > 10]


def train_topic_model(documents, n_topics=3):
    model = BERTopic(umap_model=UMAP(n_neighbors=10, n_components=2, metric="cosine", random_state=42))
    topics, probs = model.fit_transform(documents)

    # Reduce to exactly n topics
    model.reduce_topics(documents, nr_topics=n_topics)
    reduced_topics = model.topics_

    return model, reduced_topics, probs


def save_topic_words(model, topics, path):
    topic_words = ['-1: outlier']
    unique_topic_ids = sorted(set(topics) - {-1})
    for i in unique_topic_ids:
        topic_data = model.get_topic(i)[:7]
        words = [w[0] for w in topic_data]
        topic_words.append(f"{i}: " + " ".join(words))

    os.makedirs(path.parent, exist_ok=True)
    with open(path, 'w') as f:
        f.write("\n".join(topic_words))


def save_documents_to_file(documents, folder, file_name):
    os.makedirs(folder, exist_ok=True)
    with open(os.path.join(folder, file_name), 'w') as f:
        for doc in documents:
            f.write(f"{doc}\n")


def save_model(model, topics, probs, model_dir, prefix):
    os.makedirs(model_dir, exist_ok=True)
    joblib.dump(model, model_dir / f'{prefix}_model.pkl')
    joblib.dump(topics, model_dir / f'{prefix}_topics.pkl')
    joblib.dump(probs, model_dir / f'{prefix}_probs.pkl')


def save_topic_documents(documents, topics, output_dir, prefix):
    os.makedirs(output_dir, exist_ok=True)
    topic_ids = sorted(set(topics))
    for topic_id in topic_ids:
        topic_docs = [documents[i] for i in range(len(topics)) if topics[i] == topic_id]
        save_documents_to_file(topic_docs, output_dir, f'topic_{topic_id}_docs_{prefix}.txt')


def process_corpus(xml_path, output_prefix, n_topics=3):
    print(f"Processing {output_prefix}...")

    tokens = filter_tokens(extract_tokens(xml_path))
    docs = chunk_documents(tokens)

    model, topics, probs = train_topic_model(docs, n_topics=n_topics)

    # Save model and topic words
    save_model(model, topics, probs, TOPICS_MODEL_DIR, output_prefix)
    save_topic_words(model, topics, TOPIC_WORDS_DIR / f'topic_words_{output_prefix}.txt')

    # Save topic-specific documents
    save_topic_documents(docs, topics, OUTPUT_DIR / output_prefix, output_prefix)

    # Debug print
    topic_count = len(set([t for t in topics if t != -1]))
    print(f"Finished {output_prefix} with {topic_count} topics (plus outliers if any).\n")

    return model, topics, probs


# === Main execution ===

def main():
    process_corpus(DATA_DIR / "MLK_annotated" / "MLK_annotatedSpacy.xml", "MLK", n_topics=4)
    process_corpus(DATA_DIR / "CCP_annotated" / "CCP_annotatedSpacy.xml", "CCp", n_topics=4)
    print("All models, topic words, and documents saved successfully.")


if __name__ == "__main__":
    main()
