from flask import Flask, request, redirect, url_for, jsonify
import json
import requests
import pickle

import numpy as np

import ask

app = Flask(__name__)

components = ["kniazev_predicate_service", "kniazev_subject_service", "kniazev_object_service", "kniazev_natural_language_service"]
  
@app.route('/question', methods=['POST'])
def question_page():
  text = ''
  if request.method == 'POST':
    data = request.data
    question = json.loads(data)['question']
    answer = ask.ask(question, ['answer'], components)[0][5:].replace('_', ' ')
    print('Answer : {}'.format(answer))
    print('_____________________________')
    text = {
    'question': question,
    'answer': answer}
    return jsonify(text)

@app.route('/health', methods=['GET'])
def health():
  text = ''
  if request.method == 'GET':
    text = {'status': 'OK'}
    return jsonify(text)
    
if __name__ == "__main__":
  app.run(host='127.0.0.1', port=8081, debug=True)
