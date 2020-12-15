print('APP_Predicate')

import nn
import preprocessing
from dictionary import *
from predicate_nn import bag_of_words

DICT_FILE = 'dats/dict_predicate.dat'
WEIGHTS_FILE = 'dats/weights_predicate.dat'

d = DictionaryC()
d.load(DICT_FILE)

network = nn.Net()
network.load(WEIGHTS_FILE)

predicate = lambda text, res : 'http://dbpedia.org/ontology/{}'.format(vec_to_class(network.net(bag_of_words(preprocessing.full(text), d.dictionary)), d.classes))

import sys
path = '\\'.join(sys.path[0].split('\\')[:-1])
sys.path.insert(0, path)

import app_template
import return_template

configfile = "predicate.conf"
aboutendpoint = "/about"
healthendpoint = "/health"

data_type = 'predicate'
asks = []

blueprint = return_template.service(predicate, asks, data_type, configfile).relation_clf
app_template.app(configfile, aboutendpoint, healthendpoint, blueprint)
