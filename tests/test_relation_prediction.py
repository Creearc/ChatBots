import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

past_path = '\\apps\\predicate'

import sys
path = '\\'.join(sys.path[0].split('\\')[:-1])
sys.path.insert(0, '{}{}'.format(path, past_path))

import nn
import preprocessing
from dictionary import *
from predicate_nn import bag_of_words

DICT_FILE = '{}{}\\dats\\dict_predicate.dat'.format(path, past_path)
WEIGHTS_FILE = '{}{}\\dats\\weights_predicate.dat'.format(path, past_path)

d = DictionaryC()
d.load(DICT_FILE)

network = nn.Net()
network.load(WEIGHTS_FILE)

relation = lambda text : 'http://dbpedia.org/ontology/{}'.format(vec_to_class(network.net(bag_of_words(preprocessing.full(text), d.dictionary)), d.classes))

with open('test.json') as json_file:
  data = json.load(json_file)

results, etalon = [], []

for i in data:
  question = i['question']
  
  results.append(relation(question))
  etalon.append(i['predicate'])

print('______________________________________')
print('Accuracy:        {}'.format(accuracy_score(etalon, results)))
print('Precision score: {}'.format(precision_score(etalon, results, average='weighted')))
print('Recall score:    {}'.format(recall_score(etalon, results, average='weighted')))
print('F1 score:        {}'.format(f1_score(etalon, results, average='weighted')))
print('______________________________________')
