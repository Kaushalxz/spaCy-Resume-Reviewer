import spacy
import fitz  # PyMuPDF

nlp1 = spacy.load(r".\output\model-best")
doc = nlp1("there was a flight named Java")
spacy.displacy.render(doc, style="ent", jupyter=True) # display in Jupyter