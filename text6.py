from gensim import corpora, models

documents = [
    "Python for data analysis and visualization",
    "Deep learning with neural networks",
    "Statistics and probability in data science",
]

texts = [doc.lower().split() for doc in documents]
dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

lda = models.LdaModel(corpus, num_topics=2, id2word=dictionary, passes=10)
for idx, topic in lda.print_topics():
    print(f"Topic {idx}: {topic}")