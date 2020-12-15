import nn
import preprocessing
from dictionary import *
import numpy as np

def bag_of_words(text, slovar):
  out = [0 for i in range(len(slovar))]
  for word in text.split():
    if slovar.count(word) > 0:
      out[slovar.index(word)] += 1
  return out

if __name__ == '__main__':
  DICT_FILE = 'dats/dict_predicate.dat'
  DATA_FILE = 'dats/data_predicate.dat'
  WEIGHTS_FILE = 'dats/weights_predicate.dat'

  build_dict =  not True
  prepare =  not True
  train_net = not True
  re_train = True

  preprocess = True

  d = DictionaryC()

  if build_dict:
    print('Dictionary making')
    d.make('train.csv', 1, 2, preprocess)
    d.save(DICT_FILE)
    print('Done')
  else:
    print('Loading dictionary')
    d.load(DICT_FILE)
    print('Done')

  print(d.dictionary)
  print(d.classes)

  network = nn.Net(len(d.dictionary), len(d.classes))
  network.α = 0.0000002
  network.β = -0.0

  if prepare:
    print('Data preparation')
    network.D, network.Y = prepare_data('train.csv', d, bag_of_words, 1, 2, preprocess)
    network.save_data(DATA_FILE)
    print('Done')
    
  if train_net:
    if re_train:
      print('Loading weights')
      network.load(WEIGHTS_FILE)
      print('Done')
      
    print('Net training')
    network.load_data(DATA_FILE)
    iteration = 0
    while iteration < 100:
      if iteration % 10 ==0:
        network.save(WEIGHTS_FILE)
        print('{}: {}'.format(iteration, network.weights))
      for i in range(np.shape(network.weights)[0]):
        network.train(i)
      iteration  += 1
        
    print('Saving weights')
    network.save(WEIGHTS_FILE)
    print('Done')

  print('Loading weights')
  network.load(WEIGHTS_FILE)
  print('Done')

  print('Net testing')
  for text in csv_reader('test.csv'):
    text, text_class = take_info(text, 1, 2)
    if preprocess:
      text = preprocessing.full(text)
    vec = bag_of_words(text, d.dictionary)
    c_vec = class_to_vec(text_class, d.classes)

    etalon = ''.join([str(i) for i in c_vec])
    prediction = ''.join([str(i) for i in network.net(vec)])
    network.add_stats(etalon, prediction)  

  network.show_stats()
