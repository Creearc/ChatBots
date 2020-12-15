import precision_k
import threading

lock = threading.Lock()

import json
import time

import sys
path = '\\'.join(sys.path[0].split('\\')[:-1])
sys.path.insert(0, path)

import ask
components = ["kniazev_predicate_service", "kniazev_subject_service", "kniazev_object_service"]

with open('test.json') as json_file:
  data = json.load(json_file)

results, etalon = [], []
threads = 20

break_after = 40

def asker(ind):
  global data, results, etalon, threads
  count = 0
  for i in data:
    if break_after > 0 and break_after == count:
      break
    if count % threads == ind: 
      t = time.time()
      question = i['question']
      try:
        tmp = ask.ask(question, ['result'], components)
      except:
        print(question)
        continue
      with lock:
        etalon.append(i['result'])
        results.append(tmp)

      if ind == 0:
        print(count)
      res_t = time.time() - t
    count += 1

t_arr = []
for i in range(threads):
  t = threading.Thread(target=asker, args=(i,))
  t.start()
  t_arr.append(t)

for t in t_arr:
  t.join()

print(etalon)
print(results)

print('Precision@k average {}'.format(precision_k.apk(etalon, results, 10)))
print('Precision@k mean {}'.format(precision_k.mapk(etalon, results, 10)))

