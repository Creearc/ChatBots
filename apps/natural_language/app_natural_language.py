print('APP_Natural_Language')

import templates

result = lambda text, res : templates.make(res[1], res[0], res[2:])

import sys
path = '\\'.join(sys.path[0].split('\\')[:-1])
sys.path.insert(0, path)

import app_template
import return_template

configfile = "natural_language.conf"
aboutendpoint = "/about"
healthendpoint = "/health"

data_type = 'answer'

asks = ['predicate', 'subject', 'result']

blueprint = return_template.service(result, asks, data_type, configfile).relation_clf
app_template.app(configfile, aboutendpoint, healthendpoint, blueprint)
