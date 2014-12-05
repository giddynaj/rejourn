# bottle, json, pdb, bs4
# nlp, search

import bottle
from bottle import hook, post, run, get, route,  request, response
import json
import pdb
from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup as bs
import nlp
import search as sear



class EnableCors(object):
    name = 'enable_cors'
    api = 2

    def apply(self, fn, context):
        def _enable_cors(*args, **kwargs):
            # set CORS headers
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
            response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

            if bottle.request.method != 'OPTIONS':
                # actual request; reply with the actual response
                return fn(*args, **kwargs)

        return _enable_cors

app = bottle.app()

@app.route('/tags', method=['OPTIONS','DELETE'])
def dtags():
  context= request.query['context']
  tag = request.query['tag']
  q = sear.del_tags(context,tag)
  members = sear.get_tags(context)
  results = {'results' : q, 'members' : list(members)} 
  response.content_type = 'application/json' 
  return json.dumps(results)

@app.route('/tags', method=['OPTIONS','GET'])
def gtags():
  members = [""]
  hmembers = [""]
  kmembers = [""]

  if (request.query.get('keys') == 'True'):
    kmembers = sear.get_keys()

  else:
    context= request.query['context']
    members  = list(sear.get_tags(context))
    hmembers = sear.get_hash(context)

  results = {'members' : members, 'hmembers' : hmembers, 'kmembers' : kmembers} 
  response.content_type = 'application/json' 
  return json.dumps(results)

@app.route('/tags', method=['OPTIONS','POST'])
def stags():
  members = [""]
  hmembers = [""]
  kmembers = [""]

  context= request.json['context']
  tag = request.json['tag']
  if tag.find(":") > -1: 
    tag, value = tag.split(":")
    q = sear.set_hash(context,tag,value)
    hmembers = sear.get_hash(context) 
  else:
    q = sear.set_tags(context,tag)
    members = sear.get_tags(context) 

  results = {'results' : q, 'members' : list(members), 'hmembers' : hmembers } 
  response.content_type = 'application/json' 
  return json.dumps(results)

@app.route('/search', method=['OPTIONS','POST'])
def search():
  query = request.json['query']
  q = sear.return_query(query)
  results = {'results' : q} 
  response.content_type = 'application/json' 
  return json.dumps(results)

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

@app.route('/entities', method=['OPTIONS','POST'])
def named_ent():
  content = request.json['content']
  sents = nlp.word_tokenize(content)
  pos_tag = nlp.get_pos_tagger()
  pos_sents = nlp.set_pos_tags(sents,pos_tag)
  t = nlp.get_entity_tagger()
  entities = [nlp.get_entity_iobs(t.parse(pos_sent)) for pos_sent in pos_sents]
  entities = [ent for entity in entities for ent in entity]
  rne_dict = {0: 'DOCUMENT' ,
  1: 'LOCATION',
  2: 'DURATION',
  3: 'DATE',
  4: 'MEASURE',
  5: 'ORGANIZATION',
  6: 'PERSON',
  7: 'MONEY',
  8: 'CARDINAL',
  9: 'PERCENT',
  10: 'TIME'
  }
  #nlp.get_entity_iobs(entities[0])
  # maybe use zip here to replace tokens and tags lines
  tokens = [pos_token[0] for pos_sent in pos_sents for pos_token in pos_sent] 
  tags = [pos_token[1] for pos_sent in pos_sents for pos_token in pos_sent] 
  classes = set(tags)
  classes = list(classes)
  class_legend = dict((i, str(x)) for i,x in enumerate(classes))
  rclass_legend = dict((str(x), i) for i,x in enumerate(classes))
  classes = [rclass_legend[x] for x in tags]
  sent_complex = {'class_legend' : rne_dict,'tokens' : tokens, 'classes' : entities}
  response.content_type = 'application/json' 
  return json.dumps(sent_complex)

@app.route("/results/:job_key",method=['GET'])
def get_results(job_key):
  
  job = Job.fetch(job_key, connection=conn)

  if job.is_finished:
    return "Yay", 200
  else:
    return "Nay!", 202

app.install(EnableCors())

app.run(host='0.0.0.0', port=8080, debug=True)
