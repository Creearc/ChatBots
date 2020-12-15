from SPARQLWrapper import SPARQLWrapper, JSON

def get(subject, predicate, debug=False):
  subject = subject.split('/')[-1]
  predicate = predicate.split('/')[-1]
  
  s = """
  PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

  SELECT DISTINCT ?object ?objLabel
  WHERE {{
    <http://dbpedia.org/resource/{}> <http://dbpedia.org/ontology/{}> ?object .
    ?object rdfs:label ?objLabel .
    filter(LANG(?objLabel) = "en") .
  }}

  """.format(subject, predicate)
  

  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  sparql.setQuery(s)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  result = ''
  for res in results['results']['bindings']:
    result = '{}{}>, <'.format(result, res['object']['value'])
    #result = '{} {}'.format(result, res['object']['value'])

  if debug:
    print('_________________________________________________')
    print('{} {}'.format(subject, predicate))
    print('_________________________________________________')
    print(s)
    print('_________________________________________________')
    print(result)
    print('_________________________________________________')

  if len(result) > 0:
    
    return result[:-4]
  else:
    result = None

if __name__ == "__main__":
  subject, predicate = 'http://dbpedia.org/resource/Dave_Clarke_(DJ)', 'http://dbpedia.org/ontology/genre'
  print(get(subject, predicate, True))
