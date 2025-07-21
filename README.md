# Distant Reading of the African American Civil Rights Movement in the United States

**Author:** Laura Isabel Vargas García

---

## Project Overview

This project leverages **Digital Humanities** and **Natural Language Processing (NLP)** to analyze the language and themes of the African American Civil Rights Movement. By applying *distant reading* techniques, it explores the fight against racial segregation in the United States through two key corpora:

- **Colored Conventions Project (CCP):** Documents from Black conventions held between the mid-19th and early 20th centuries, organized by free Black community leaders in the North.
- **Martin Luther King Jr. (MLK) Speeches:** A collection of 11 speeches from the 1950s and 1960s, focused on racial equality, social justice, and nonviolent resistance.

---

## Project Structure

The project is organized into several main scripts and data folders:

- **Data Preprocessing:** Cleaning and preparing raw text data, including stopword and punctuation removal using spaCy.
- **XML Conversion:** Transforming cleaned texts into XML format with metadata, POS tags, and named entity annotations.
- **Collocation Analysis:** Extracting and analyzing frequent word pairs (*bigrams*) from the corpora.
- **NER Analysis:** Identifying and counting the most frequent named entities, excluding numbers and locations.
- **Topic Modeling:** Filtering tokens by grammatical category and entity type, segmenting texts, and applying the BERTopic model.

---

## Methodology

1. **Preprocessing:**
   - Used `spaCy` (`en_core_web_sm`) to clean texts by removing stopwords and punctuation.

2. **XML Conversion:**
   - Converted texts to XML.
   - Extracted metadata and annotated with POS tags and named entities.

3. **Collocation Analysis:**
   - Extracted tokens from XML.
   - Generated bigrams and identified the most frequent collocations in each corpus.

4. **Named Entity Recognition (NER):**
   - Identified the 20 most frequent named entities.
   - Filtered out numbers and locations to focus on relevant people, organizations, and concepts.

5. **Topic Modeling:**
   - Filtered for nouns, adjectives, proper nouns, and relevant named entities.
   - Segmented data into smaller documents.
   - Applied `BERTopic` to extract and compare core topics in MLK and CCP texts.

---

## Key Results

### **Collocations**

- **MLK:**  
  `United States`, `freedom ring`, `let march`, `civil rights`, `direct action`, `God children`, `Abraham Lincoln`, `let freedom`, `let dissatisfied`, `New York`, `love enemies`, `stop help`, `years ago`, `dream day`, `Montgomery Alabama`

- **CCP:**  
  `colored people`, `United States`, `New York`, `Colored men`, `J.H`, `Vice President`, `people State`, `W.H`, `J.W`, `equal rights`, `white men`

---

### **Named Entities**

- **MLK:**  
  `Negro`, `today`, `Jesus`, `American`, `South`, `tonight`, `Love`, `Christian`, `morning`, `years`, `Abraham Lincoln`, `Vietnamese`, `French`, `Americans`, `Christians`, `Negroes`, `John`, `Diem`, `Stanton`, `tomorrow`

- **CCP:**  
  `Convention`, `State`, `American`, `South`, `Committee`, `Congress`, `Business Committee`, `Negro`, `Constitution`, `years`, `Association`, `Republican`, `evening`, `second`, `1865`, `annual`, `Executive Committee`, `Christian`, `Resolved Convention`, `Africa`

---

### **Topic Modeling**

#### **MLK Speeches**

- **Opposition to Violence**
  - **Key terms:** `negro`, `nation`, `freedom`, `sir`, `people`, `white`, `men`
  - Focuses on civil rights, denounces violence and inaction, emphasizes justice and leadership.

- **Christian Tone**
  - **Key terms:** `love`, `life`, `God`, `right`, `morning`, `man`, `people`
  - Highlights love for enemies, Christian philosophy, and moral reflection.

#### **CCP Documents**

- **Institutional Tone and Main Concern**
  - **Key terms:** `convention`, `state`, `committee`, `people`, `mr`, `colored`, `men`
  - Formal, political discourse on emancipation, enfranchisement, and dignity.

- **Concern about Cuba**
  - **Key terms:** `cuba`, `Spanish`, `government`, `slavery`, `island`, `spain`, `Cuban`
  - Discusses slavery in Cuba, US intervention, and the broader political context.

- **Education Issue**
  - **Key terms:** `Kentucky`, `Frankfort`, `Lexington`, `association`, `Henderson`, `convention`, `Louisville`
  - Focuses on educational advancement and legislative reform in Kentucky conventions.

---

##  How to Run

1. **Install Dependencies**
   - Ensure Python 3.x is installed.
   - Install required packages

2. **Prepare Data**
   - Place raw corpora in the appropriate `data/` folders.

3. **Run Preprocessing Scripts**
   - Execute scripts for cleaning, XML conversion, and annotation.

4. **Run Analysis Scripts**
   - Execute scripts for collocation analysis, NER, and topic modeling.

5. **Review Results**
   - Results will be saved to the `output/` folder and may include visualizations (e.g., word clouds, topic summaries).

---

## Dependencies

- Python 3.x  
- [`spaCy`](https://spacy.io/) (`en_core_web_sm`)  
- [`BERTopic`](https://maartengr.github.io/BERTopic/)  

---

## Acknowledgments

- [Colored Conventions Project](https://www.coloredconventions.org/)  
- MLK Speeches courtesy of the **Richton Park Library MLK Program**

---
