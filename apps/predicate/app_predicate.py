print('APP_Predicate')
path = '/home/students/stalknia/Papka/apps/'
import nn
import preprocessing
from dictionary import *
from predicate_nn import bag_of_words

DICT_FILE = '{}predicate/dats/dict_predicate.dat'.format(path)
WEIGHTS_FILE = '{}predicate/dats/weights_predicate.dat'.format(path)

d = DictionaryC()
d.load(DICT_FILE)

network = nn.Net()
network.load(WEIGHTS_FILE)

predicate = lambda text, res : 'http://dbpedia.org/ontology/{}'.format(vec_to_class(network.net(bag_of_words(preprocessing.full(text), d.dictionary)), d.classes))

import sys
sys.path.insert(0, path)
import app_template
import return_template

configfile = "{}predicate/predicate.conf".format(path)
aboutendpoint = "/about"
healthendpoint = "/health"

data_type = 'predicate'
asks = []

blueprint = return_template.service(predicate, asks, data_type, configfile).relation_clf
app_template.app(configfile, aboutendpoint, healthendpoint, blueprint)
