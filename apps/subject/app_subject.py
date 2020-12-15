print('APP_Subject')

import named_entities

subject = lambda text, res : named_entities.best(text)

import sys
path = '\\'.join(sys.path[0].split('\\')[:-1])
sys.path.insert(0, path)

import app_template
import return_template

configfile = "subject.conf"
aboutendpoint = "/about"
healthendpoint = "/health"

data_type = 'subject'
asks = []

blueprint = return_template.service(subject, asks, data_type, configfile).relation_clf
app_template.app(configfile, aboutendpoint, healthendpoint, blueprint)
