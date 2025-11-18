from textblob import TextBlob


def analyze_sentiment(text):
    # Create a TextBlob object
    blob = TextBlob(text)

    # Analyze the sentiment
    sentiment = blob.sentiment

    # Print the results
    print(f"Text: {text}")
    print(f"Polarity: {sentiment.polarity}")  # Polarity ranges from -1 (negative) to 1 (positive)
    print(f"Subjectivity: {sentiment.subjectivity}")  # Subjectivity ranges from 0 (objective) to 1 (subjective)


# Example texts
texts = [
    "I love this product! It's amazing.",
    "This is the worst experience I've ever had.",
    "The service was okay, nothing special.",
    "Absolutely fantastic! Will buy again.",
    "I'm not sure how I feel about this."
]

# Analyze the sentiment of each text
for text in texts:
    analyze_sentiment(text)
    print()