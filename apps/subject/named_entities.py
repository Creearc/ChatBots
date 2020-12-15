import requests
import time

def named_entity_linking(text, confidence=0.5):
  params = {'text' : text, 'confidence' : confidence}

  response = requests.get(url='http://webengineering.ins.hs-anhalt.de:43720/rest/annotate',
                          params=params,
                          headers={'accept': 'application/json'},
                          verify=False)

  response = response.json()
  return response

def get_urls(data):
  out = []
  if 'Resources' in data.keys():
    data = data['Resources']
    for i in data:
      out.append({i['@URI'] : i['@surfaceForm']})
    return out

def best(text):
  conf = 0.9
  res = None
  while res == None and conf > 0:
    res = get_urls(named_entity_linking(text, conf))
    print(conf)
    conf -= 0.1
  if res is None:
    return None
  else:
    return list(res[0].keys())[0]

if __name__ == "__main__":
  questions = ['what genre of music does mike dirnt produce',
               ' What soccer position does matt heath play',
               'which english city was david buck born in',
               'where was albert belle born?',
               'who wrote la reine margot',
               'Where was fritz hohn born',
               'Who wrote the pigman & me?',
               'Where in asia was sam yoon born']
  for q in questions:
    t = time.time()
    print(best(q))
    print(time.time() - t)
