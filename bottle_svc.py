import bottle
from bottle import hook, post, run, get, route,  request, response
import json
import pdb
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup as bs
import nlp
from pygoogle import pygoogle as pg

class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

app = bottle.app()

@app.route('/search', method=['OPTIONS','POST'])
def search():
  query = request.json['query']
  g = pg(query)
  results = g.search()
  pdb.set_trace() 
  sent_complex = {'class_legend' : { 0 : 'content', 1 : 'not-content', 2:'extra' },'sentences' : sent_tokenize_list, 'classes' : [0 for sent in sent_tokenize_list]}
  response.content_type = 'application/json' 
  return json.dumps(sent_complex)

@app.route('/tokenize_sent', method=['OPTIONS','POST'])
def tokenize_sent():
  content = request.json['content']
  soup = bs(content)
  soup = soup.get_text()
  sent_tokenize_list = sent_tokenize(soup) 
  sent_complex = {'class_legend' : { 0 : 'content', 1 : 'not-content', 2:'extra' },'sentences' : sent_tokenize_list, 'classes' : [0 for sent in sent_tokenize_list]}
  response.content_type = 'application/json' 
  return json.dumps(sent_complex)

@app.route('/get_sent', method=['OPTIONS','POST'])
def get_sent():
  content = request.json['content']
  classes = request.json['classes']
  nlp.receive_content(classes,content)
  return {'result' : 'success'}

@app.route('/assign_pos', method=['OPTIONS','POST'])
def assign_pos():
  content = request.json['content']
  sents = nlp.word_tokenize(content)
  pos_tag = nlp.get_pos_tagger()
  pos_sents = nlp.set_pos_tags(sents,pos_tag)
  tokens = [pos_token[0] for pos_sent in pos_sents for pos_token in pos_sent] 
  tags = [pos_token[1] for pos_sent in pos_sents for pos_token in pos_sent] 
  classes = set(tags)
  classes = list(classes)
  class_legend = dict((i, str(x)) for i,x in enumerate(classes))
  rclass_legend = dict((str(x), i) for i,x in enumerate(classes))
  classes = [rclass_legend[x] for x in tags]
  sent_complex = {'class_legend' : class_legend,'tokens' : tokens, 'classes' : classes}
  response.content_type = 'application/json' 
  return json.dumps(sent_complex)


app.install(EnableCors())

app.run(host='0.0.0.0', port=8080, debug=True)
