from sklearn.feature_extraction.text import TfidfVectorizer

docs = [
    "Python is great for data science",
    "Data science includes machine learning",
    "Python and ML go hand in hand"
]

vectorizer = TfidfVectorizer()
X = vectorizer.fit_transform(docs)

print(vectorizer.get_feature_names_out())
print(X.toarray())