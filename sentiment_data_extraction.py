import spacy
from textblob import TextBlob

# Load the spaCy model
nlp = spacy.load("en_core_web_sm")


def extract_facts(text):
    # Process the text with spaCy
    doc = nlp(text)

    # Extract named entities
    entities = []
    for ent in doc.ents:
        entities.append((ent.text, ent.label_))

    persons = []
    for ent in doc.ents:
        if ent.label_ in "PERSON":
            persons.append(ent.text)

    # Extract numbers and dates
    numbers = []
    for ent in doc.ents:
        if ent.label_ in ("CARDINAL", "QUANTITY", "PERCENT", "MONEY"):
            numbers.append(ent.text)

    dates = []
    for ent in doc.ents:
        if ent.label_ in ("DATE", "TIME"):
            dates.append(ent.text)

    return entities, list(set(persons)), numbers, dates


def analyze_sentiment(text):
    # Create a TextBlob object
    blob = TextBlob(text)

    # Analyze the sentiment
    sentiment = blob.sentiment

    # Polarity ranges from -1 (negative) to 1 (positive)
    # Subjectivity ranges from 0 (objective) to 1 (subjective)
    return sentiment.polarity, sentiment.subjectivity


# Example texts
texts = [
    "Alice: Hey everyone, I wanted to talk about global warming. It's such a pressing issue, and I think we should brainstorm some solutions. I've come across five possible ones: stopping fossil fuels and switching to renewable fuels, planting more trees, capturing carbon from the atmosphere and burying it underground using advanced technology, capturing carbon by growing more algae in oceans, and reflecting back sunlight using advanced technology. What do you all think?"
    "Bob: Honestly, I think stopping fossil fuels and switching to renewable fuels is the most impactful solution. Fossil fuels are the main source of greenhouse gases. Transitioning to renewable energy like solar and wind could drastically reduce emissions."
    "Cathy: I completely agree, Bob. Stopping fossil fuels should be our top priority. Renewable energy sources are becoming more viable and cost-effective. We need to invest in these technologies on a massive scale."
    "David: Exactly. The technology for renewable energy is already here and continuously improving. It’s about scaling up our efforts and transitioning away from fossil fuels as quickly as possible."
    "Eva: Yes, focusing on renewable energy addresses the root cause of global warming. Planting trees and other methods are helpful, but they don’t eliminate the problem at its source like moving away from fossil fuels does."
    "Frank: We should push for policies that support renewable energy development and penalize fossil fuel consumption. Tax incentives for clean energy projects and higher carbon taxes could drive significant change."
    "Grace: That’s right. By making renewable energy more attractive and affordable, we can shift the energy market. Governments need to take the lead with strong policies and subsidies for clean energy."
    "Helen: Public education is also crucial. Many people are still unaware of the benefits and feasibility of renewable energy. We need to spread awareness to gain broader support."
    "Ivy: Agreed. Increasing public awareness and support can lead to more political action. We need a global movement towards renewable energy adoption."
    "Jack: And let’s not forget the economic benefits. Transitioning to renewable energy can create new jobs in manufacturing, installation, and maintenance. It’s beneficial for both the economy and the environment."
    "Alice: It sounds like we all agree that stopping fossil fuels and switching to renewable fuels is the most effective solution. It addresses the root of the problem and has numerous additional benefits."
    "Bob: Yes, and it’s not just about reducing emissions. Renewable energy also helps reduce air and water pollution, which has immediate health benefits for communities."
    "Cathy: Plus, renewable energy sources are sustainable in the long term. Fossil fuels are finite, but the sun and wind are virtually limitless. Investing in these sources now is crucial for our future."
    "David: We should also support research and development in energy storage and grid management. These areas are key to making renewable energy reliable and efficient."
    "Eva: Exactly. With better storage solutions, we can ensure a steady energy supply even when the sun isn’t shining or the wind isn’t blowing."
    "Frank: Let’s commit to supporting renewable energy in our daily lives as well. Choose green energy options where available, reduce our own carbon footprints, and advocate for change."
    "Grace: I’m on board with that. Every small step we take contributes to a larger movement. Let’s be vocal advocates for renewable energy."
    "Helen: It’s great to see us all united on this. Let’s keep pushing for this change and support each other in making sustainable choices."
    "Ivy: Agreed. Thanks for the discussion, everyone. Let’s stay committed and make a real impact on reducing global warming by stopping fossil fuels and switching to renewable fuels."
    "Jack: Thanks, everyone. Together, we can make a difference. Let’s do this!"
]

# Analyze each text
for text in texts:
    entities, persons, numbers, dates = extract_facts(text)
    polarity, subjectivity = analyze_sentiment(text)

    print(f"Text: {text}")
    print(f"Entities: {entities}")
    print(f"Persons: {persons}")
    print(f"Numbers: {numbers}")
    print(f"Dates: {dates}")
    print(f"Polarity: {polarity}")
    print(f"Subjectivity: {subjectivity}")
    print()
