import requests
from qanary_helpers.qanary_queries import query_triplestore
import json

qanary_pipeline_url = "http://webengineering.ins.hs-anhalt.de:43740/startquestionansweringwithtextquestion"

def get_text_response(triplestore_endpoint, graph, SPARQLquery):
    text_response = None
    result = query_triplestore('{}/query'.format(triplestore_endpoint), graph, SPARQLquery)

    out = []
    for binding in result['results']['bindings']:
        out.append(binding['o']['value'])
    return out

def get_final_result(asks, endpoint, in_graph):
    s = ''
    for l in asks:
        s = '{}oa:{} '.format(s, l)
    SPARQLquery = """
        PREFIX oa: <http://www.w3.org/ns/openannotation/core/>
        SELECT ?p ?o 
        FROM <{graph_guid}>
        WHERE 
        {{
            VALUES ?p {{ {s} }}. 
            ?s ?p ?o .
        }}""".format(graph_guid=in_graph, s=s)

    return get_text_response(triplestore_endpoint=endpoint, 
                             graph=in_graph,
                             SPARQLquery=SPARQLquery)


def ask(question_text, result_type, component):
  response = requests.post(url=qanary_pipeline_url,
                             params={
                                 "question": question_text,
                                 "componentlist[]": component
                             }).json()
  result = get_final_result(result_type, response['endpoint'], response['inGraph'])
  return result


if __name__ == "__main__":
    components = ["kniazev_predicate_service", "kniazev_subject_service", "kniazev_object_service", "kniazev_natural_language_service"]
    #print(ask('what genre of music does mike dirnt produce', ["kniazev_predicate_service", "kniazev_subject_service", "kniazev_object_service", "kniazev_natural_language_service"]))
    #print(ask('where was albert belle born?', ["kniazev_predicate_service", "kniazev_subject_service", "kniazev_object_service", "kniazev_natural_language_service"]))
    print(ask_raw('what genre of music does mike dirnt produce', ['predicate', 'subject', 'result', 'answer'], components))
    

