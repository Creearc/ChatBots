print('APP_Subject')


tts = lambda text, res : text

import sys
path = '\\'.join(sys.path[0].split('\\')[:-1])
sys.path.insert(0, path)

import app_template
import return_template

configfile = "tts.conf"
aboutendpoint = "/about"
healthendpoint = "/health"

data_type = 'result'
asks = []

blueprint = return_template.service(tts, asks, data_type, configfile).relation_clf
app_template.app(configfile, aboutendpoint, healthendpoint, blueprint)
