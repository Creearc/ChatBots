from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import numpy as np

import pickle

class Net:
  def __init__(self, input_count=6, neuron_count=6):
    self.input_count = input_count
    self.neuron_count = neuron_count

    self.weights = np.zeros((neuron_count, input_count))
    self.D = None # inputs
    self.Y = None # answers
    
    self.σ = lambda x: 1 if x > 0.9 else 0
    self.α = 0.02
    self.β = 0.0

    self.etalons, self.predictions = [], []


  def funk(self, x, i):
      s = self.β + np.sum(x @ self.weights[i])
      return self.σ(s)
   
  def train(self, i):
    _w = self.weights[i].copy()
    for x, y in zip(self.D, self.Y[i]):
        self.weights[i] += self.α * (y - self.funk(x, i)) * x
    return (self.weights[i] != _w).any()

  def net(self, vec, other=False):
    s = [0 for i in range(np.shape(self.weights)[0])]
    for i in range(len(s)):
      s[i] = self.funk(vec, i)
      if s[i] == 1:
        other = True
        break
    if not other:
      s[0] = 1
    return(s)

  def load(self, WEIGHTS_FILE='weights.dat'):
    with open(WEIGHTS_FILE, 'rb') as f:
      self.weights = pickle.load(f)

  def save(self, WEIGHTS_FILE='weights.dat'):
    with open(WEIGHTS_FILE, "wb") as f:
      pickle.dump(self.weights, f)

  def load_data(self, DATA_FILE='data.dat'):
    with open(DATA_FILE, 'rb') as f:
      out = pickle.load(f)
    self.D, self.Y = out[0], out[1]

  def save_data(self, DATA_FILE='data.dat'):
    with open(DATA_FILE, "wb") as f:
      pickle.dump([self.D, self.Y], f)

  def add_stats(self, etalon, prediction):
    self.etalons.append(etalon)
    self.predictions.append(prediction)

  def clear_stats(self, etalon, prediction):
    self.etalons = []
    self.predictions = []

  def show_stats(self):
    print('Accuracy:        {}'.format(accuracy_score(self.etalons, self.predictions)))
    print('Precision score: {}'.format(precision_score(self.etalons, self.predictions, average='weighted')))
    print('Recall score:    {}'.format(recall_score(self.etalons, self.predictions, average='weighted')))
    print('F1 score:        {}'.format(f1_score(self.etalons, self.predictions, average='weighted')))
    
