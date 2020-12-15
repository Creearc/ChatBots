import re
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
import string

from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
def lemmatize_words(text):
  return " ".join([lemmatizer.lemmatize(word) for word in text.split()])

from nltk.stem.porter import PorterStemmer
stemmer = PorterStemmer()
def stem_words(text):
  return " ".join([stemmer.stem(word) for word in text.split()])
  
from nltk.corpus import stopwords
STOPWORDS = set(stopwords.words('english'))
def remove_stopwords(text):
  return " ".join([word for word in str(text).split() if word not in STOPWORDS])

PUNCT_TO_REMOVE = string.punctuation
def remove_punctuation(text):
  return text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))

def remove_numbers(text):
  return " ".join([word for word in text.split() if word.isalpha()])

def full(text, lemmatize=False):
  text = text.translate(str.maketrans('', '', PUNCT_TO_REMOVE)).lower()
  text = [word for word in text.split() if word.isalpha()]
  text = [word for word in text if word not in STOPWORDS]
  if lemmatize:
    text = [lemmatizer.lemmatize(word) for word in text]
  else:
    text = [stemmer.stem(word) for word in text]
  return " ".join(text)


if __name__ == '__main__':
  text = 'Just sim8le text, for test!'
  text = remove_punctuation(text.lower())
  text = remove_numbers(text)
  text = remove_stopwords(text)
  text = stem_words(text)
  print(text)
  text = 'Just sim8le text, for test!'
  print(full(text))
