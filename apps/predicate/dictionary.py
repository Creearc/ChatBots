import preprocessing
import pickle
import numpy as np
import csv

class DictionaryC:
  def __init__(self):
    self.dictionary = []
    self.classes = []
    self.c = []

  def make(self, filename, ind1=0, ind2=1, preprocess=False):
    self.dictionary = set()
    self.classes  = set()
    for text in csv_reader(filename):
      text, text_class = take_info(text, ind1, ind2)
      if preprocess:
        text = preprocessing.full(text)
      self.classes.add(text_class)
      for word in text.split():
        self.dictionary.add(word)

    self.dictionary = list(self.dictionary)
    self.dictionary.sort()
    self.classes = list(self.classes)
    self.classes.sort()

  def load(self, DICT_FILE):
    with open(DICT_FILE, 'rb') as f:
      out = pickle.load(f)
    self.dictionary, self.classes = out[0], out[1]

  def save(self, DICT_FILE):
    with open(DICT_FILE, "wb") as f:
      pickle.dump([self.dictionary, self.classes], f)


def take_info(text, ind1=0, ind2=1):
  text, text_class = text[ind1], text[ind2].split('/')[-1]
  return text, text_class

def prepare_data(filename, d, function, ind1=0, ind2=1, preprocess=False):
  D = None
  for text in csv_reader(filename):
    text, text_class = take_info(text, ind1, ind2)
    if preprocess:
      text = preprocessing.full(text)
    vec = function(text, d.dictionary)
    c_vec = class_to_vec(text_class, d.classes)
    if D is None:
      D = vec
      Y = c_vec
    else:
      D = np.vstack((D, vec))
      Y = np.vstack((Y, c_vec))
  Y = np.swapaxes(Y, 0, 1)
  return D, Y

def csv_reader(filename):
  with open(filename, newline='') as csvfile:
    f = csv.reader(csvfile, delimiter=';', quotechar='"')
    for text in f:
      yield text

def vec_to_str(vec):
  return ''.join([str(i) for i in vec])

def class_to_vec(class_name, classes):
    out = [0 for i in range(len(classes))]
    out[classes.index(class_name)] = 1
    return out

def vec_to_class(vec, classes):
  if vec.count(1) > 0:
    return classes[vec.index(1)]
  else:
    return 'Other'
