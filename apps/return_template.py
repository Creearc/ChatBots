from flask import Blueprint, jsonify, request
from qanary_helpers.configuration import Configuration
from qanary_helpers.qanary_queries import get_text_question_in_graph, insert_into_triplestore
import requests
import json
import logging

import sys
path = '\\'.join(sys.path[0].split('\\')[:-1])
sys.path.insert(0, path)

import ask

class service:
    def __init__(self, function, asks, data_type, configfile):
        self.function = function
        self.asks = asks

        #logging.basicConfig(format='%(asctime)s - %(message)s', level=logging.INFO)
        self.relation_clf = Blueprint('relation_clf', __name__, template_folder='templates')

        configuration = Configuration(configfile, [
            'servicename',
            'serviceversion'
        ])


        @self.relation_clf.route("/annotatequestion", methods=['POST'])
        def qanary_service():
            """the POST endpoint required for a Qanary service"""

            triplestore_endpoint = request.json["values"]["urn:qanary#endpoint"]
            triplestore_ingraph = request.json["values"]["urn:qanary#inGraph"]
            triplestore_outgraph = request.json["values"]["urn:qanary#outGraph"]

            #logging.info(
            #    "endpoint: %s, inGraph: %s, outGraph: %s" % (triplestore_endpoint, triplestore_ingraph, triplestore_outgraph))

            text = get_text_question_in_graph(triplestore_endpoint=triplestore_endpoint, graph=triplestore_ingraph)[0]['text']

            #logging.info(f'Question Text: {text}')

            res = ask.get_final_result(self.asks, triplestore_endpoint, triplestore_ingraph)

            text = self.function(text, res)
            #logging.info(f'Answer Text: {text}')

            SPARQLquery = """
            PREFIX qa: <http://www.wdaqua.eu/qa#>
            PREFIX oa: <http://www.w3.org/ns/openannotation/core/>
            PREFIX dbo: <http://dbpedia.org/ontology/>

            INSERT {{
            GRAPH <{uuid}> {{
              ?a oa:{data_type}  <{data_uri}>  .
              ?a oa:annotatedBy <urn:qanary:{app_name}> .
              ?a oa:annotatedAt ?time .
              }}
            }}
            WHERE {{
              BIND (IRI(str(RAND())) AS ?a) .
              BIND (now() as ?time) 
            }}
            """.format(
                uuid=triplestore_ingraph,
                app_name="{0}:{1}:Python".format(configuration.servicename, configuration.serviceversion),
                data_uri = text,
                data_type = data_type
            )  # building SPARQL query

            #logging.info(f'SPARQL: {SPARQLquery}')

            insert_into_triplestore(triplestore_endpoint, triplestore_ingraph,
                                    SPARQLquery)  # inserting new data to the triplestore

            return jsonify(request.get_json())


        @self.relation_clf.route("/", methods=['GET'])
        def index():
            """an example GET endpoint returning "hello world (String)"""

            #logging.info("host_url: %s" % (request.host_url,))
            return "Hi! \n This is component."

