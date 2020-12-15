print('APP_Object')
path = '/home/students/stalknia/Papka/apps/'
import sparql

objectt = lambda text, res : sparql.get(res[0], res[1])

import sys
sys.path.insert(0, path)
import app_template
import return_template

configfile = "{}object/object.conf".format(path)
aboutendpoint = "/about"
healthendpoint = "/health"

data_type = 'result'

asks = ['subject', 'predicate']

blueprint = return_template.service(objectt, asks, data_type, configfile).relation_clf
app_template.app(configfile, aboutendpoint, healthendpoint, blueprint)
