from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from collections import Counter

nltk.download('punkt')
nltk.download('stopwords')

text = "Python is an great programming language. It is great for data science and great for web development. Great!"

# Tokenize
tokens = word_tokenize(text.lower())

# Remove stopwords and punctuation
filtered = [word for word in tokens if word.isalpha() and word not in stopwords.words('english')]

print(filtered)

word_freq = Counter(filtered)
print(word_freq.most_common())

text_str = " ".join(filtered)
wordcloud = WordCloud(width=600, height=400, background_color='white').generate(text_str)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.show()