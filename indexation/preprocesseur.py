import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

STOPWORDS = set(stopwords.words("french") + stopwords.words("english"))
stemmer = PorterStemmer()

def preprocess(text):
    text = text.lower()
    tokens = re.findall(r'\b[a-zA-ZÀ-ÿ]{2,}\b', text)
    tokens = [t for t in tokens if t not in STOPWORDS]
    # optional stemming:
    # tokens = [stemmer.stem(t) for t in tokens]
    return tokens