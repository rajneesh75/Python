from textblob import TextBlob

text = "I love Python. It is such a versatile and powerful programming language!"
blob = TextBlob(text)

print(blob.sentiment)