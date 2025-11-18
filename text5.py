import spacy
nlp = spacy.load("en_core_web_sm")

doc = nlp("Elon Musk founded SpaceX in California.")
for ent in doc.ents:
    print(ent.text, ent.label_)