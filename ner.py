import spacy
import pickle
import random

train_data = pickle.load(open(r"C:\Users\Kaushal\Downloads\train_data.pkl", "rb"))
nlp = spacy.blank('en')
print(train_data[0])

def train_model(train_data):
    # Check if 'ner' is not in the pipeline and add it
    if 'ner' not in nlp.pipe_names:
        nlp.add_pipe("ner", last=True)
    ner = nlp.get_pipe("ner")
    
    # Add labels
    for _, annotation in train_data:
        for ent in annotation['entities']:
            ner.add_label(ent[2])
            
    # Disable other pipes during training
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != 'ner']
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(10):
            print("Starting iteration " + str(itn))
            random.shuffle(train_data)
            losses = {}
            for text, annotations in train_data:
                try:
                    nlp.update(
                        [text],  # batch of texts
                        [annotations],  # batch of annotations
                        drop=0.2,  # dropout - make it harder to memorise data
                        sgd=optimizer,  # callable to update weights
                        losses=losses)
                except Exception as e:
                    pass
                
            print(losses)

train_model(train_data)
nlp.to_disk('nlp_model')
nlp_model = spacy.load('nlp_model')


doc = nlp_model(train_data[0])
for ent in doc.ents:
    print(f'{ent.label_.upper():{30}}- {ent.text}')