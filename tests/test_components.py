import precision_k
import threading

lock = threading.Lock()

import json
import time
import pickle

def load(filename):
  with open(filename, 'rb') as f:
    out = pickle.load(f)
  return out

def save(filename, var):
  with open(filename, "wb") as f:
    pickle.dump(var, f)

import sys
path = '\\'.join(sys.path[0].split('\\')[:-1])
sys.path.insert(0, path)

import ask
components = ["kniazev_predicate_service", "kniazev_subject_service", "kniazev_object_service", "kniazev_natural_language_service"]

with open('test.json') as json_file:
  data = json.load(json_file)

out = [0 for i in range(len(components))]
threads = 20

break_after = 20

def asker(ind):
  global data, out, threads
  count = 0
  for i in data:
    if break_after > 0 and break_after == count:
      break
    if count % threads == ind: 
      t = time.time()
      question = i['question']
      tmp = ask.ask(question, ['predicate', 'subject', 'result', 'answer'], components)
      res = [tmp[1], tmp[0], tmp[2 : -1], tmp[-1]]
      with lock:
        for i in range(len(tmp)):
          if res[i] == 'None':
            out[i] += 1

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

print(out)

