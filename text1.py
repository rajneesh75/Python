import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter


nltk.download('punkt')
nltk.download('stopwords')

text = "Python is an amazing programming language. It is great for data science and web development!"

# Tokenize
tokens = word_tokenize(text.lower())

# Remove stopwords and punctuation
filtered = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]

print(filtered)

word_freq = Counter(filtered)
print(word_freq.most_common())