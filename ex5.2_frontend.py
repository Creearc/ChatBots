from flask import Flask, request, redirect, url_for
import requests

SERVER_IP = 'http://127.0.0.1:8081'

app = Flask(__name__)

def check(url):
  url = '{}/health'.format(url)
  try:
    response = requests.get(url=url)
    out = response.json()
    return out
  except:
    return {'status': 'NOT_OK'}
  

def ask(url, question_text):
  url = '{}/question'.format(url)
  data = {'question' : question_text}
  response = requests.post(url=url, json=data)
  out = response.json()
  return out
   
@app.route('/', methods=['GET', 'POST'])
def index():
  text = ''
  if request.method == 'POST':
    question = request.form['question']
    if question != '': 
      text = check(SERVER_IP)
      if text['status'] == 'OK':
        text = ask(SERVER_IP, question)
        text = '''
              Question : {}<br>
              Answer : {}<br>'''.format(text['question'],
                                         text['answer'])
  return '''
  <table border=10 width=70% cellspacing=10> <tr><td><br>
  <form action="" method=post enctype=application/json>
      <input type=text name=question size=100>
      <input type=submit value=Ask!>
  </form></td></tr>
  <tr><td>{}
  </td></tr></table>'''.format(text)

if __name__ == "__main__":
  app.run(host='127.0.0.1', port=8000, debug=True)
