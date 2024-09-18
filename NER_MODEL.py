import spacy
import fitz  # PyMuPDF
import json
import pandas as pd
import os
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin
import pickle
import random

TRAIN_DATA = []
# Specify the encoding as UTF-8
train_data = pickle.load(open(r"C:\Users\Kaushal\Downloads\train_data.pkl", "rb"))


# nlp = spacy.blank('en')

for text, annotations in train_data:
    TRAIN_DATA.append((text,annotations['entities']))

#nlp = spacy.blank("en") # load a new spacy model
nlp = spacy.load("en_core_web_sm") # load other spacy model

db = DocBin() # create a DocBin object
import logging
for text, annot in tqdm(TRAIN_DATA):
    doc = nlp.make_doc(text)  # Create a Doc without running the pipeline
    ents = list(doc.ents)  # Start with existing entities
    for start, end, label in annot:
        # Check against both manually added and pre-existing entities to avoid overlaps
        is_overlapping = any(start < existing_ent.end and end > existing_ent.start for existing_ent in ents)
        if is_overlapping:
            #logging.warning(f"Skipping overlapping entity: {label} ({start}, {end})")
            continue
        span = doc.char_span(start, end, label=label, alignment_mode="strict")
        if span is None:
            #logging.info(f"Skipping entity due to char_span returning None: {label} ({start}, {end})")
            continue
        ents.append(span)  # Add new entity if no overlap and valid span
    # Attempt to reconcile and set entities
    try:
        doc.ents = ents
    except ValueError as e:
        #logging.error(f"Error setting entities: {e}")
        continue
    db.add(doc)

#os.chdir(r'XXXX\XXXXX')
db.to_disk("./train.spacy") # save the docbin object

#TESTING
nlp1 = spacy.load(r"C:\Users\Kaushal\Downloads\output\model-best")
# nlp.add_pipe('sentencizer')
# doc = nlp1("""I am a Java Developer with 5 years of experience in Java, Spring, and Hibernate.""")

# Print entities in the text
# for ent in doc.ents:
#     # Print the entity text and its label
#     print(f"{ent.text}: {ent.label_}")

# doc = nlp1(train_data[0][0])
# for ent in doc.ents:
#     print(f'{ent.label_.upper():{30}}- {ent.text}')


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text()
    return text

# Function to process text and print entities
def print_entities_from_text(text):
    doc = nlp1(text)
    for ent in doc.ents:
        print(f'{ent.label_.upper():{30}}- {ent.text}')

# Path to your resume PDF
resume_path = r"C:\Users\Kaushal\Downloads\KaushalResume.docx.pdf"

# Extract text from your resume
resume_text = extract_text_from_pdf(resume_path)

# Print entities identified in your resume
print_entities_from_text(resume_text)