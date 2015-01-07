import bottle
from bottle import hook, post, run, get, route,  request, response
import json
import pdb
from time import sleep
from rq import Queue
from rq.job import Job
from worker import conn
import rejourn

q = Queue(connection=conn)

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
  results = rejourn.delete_tags(context,tag)
  return json.dumps(results)

@app.route('/tags', method=['OPTIONS','GET'])
def gtags():
  keys = request.query.get('keys')
  context= request.query['context']
  results = rejourn.get_tags(keys,context)
  return json.dumps(results)

@app.route('/tags', method=['OPTIONS','POST'])
def stags():
  context= request.json['context']
  tag = request.json['tag']
  results = rejourn.set_tags(tag,context)
  return json.dumps(results)

@app.route('/search', method=['OPTIONS','POST'])
def search():
  query = request.json['query']
  results = rejourn.get_search(query)
  pdb.set_trace()
  return json.dumps(results)

@app.route('/tokenize_sent', method=['OPTIONS','POST'])
def tokenize_sent():
  content = request.json['content']
  if False:
    job = q.enqueue_call(
      func=rejourn.get_tokenized_sentences,
      args=(content,),
      result_ttl=5000
    )
    return json.dumps({'job_id':job.get_id()})
  else:
    results = rejourn.get_tokenized_sentences(content)
    return json.dumps(results)

@app.route('/get_sent', method=['OPTIONS','POST'])
def get_sent():
  request_type = request.json['request_type']
  content = request.json['content']
  classes = request.json['classes']
  job = q.enqueue_call(
    func=rejourn.save_training, 
    args=(request_type,classes,content), 
    result_ttl=5000
  )
  #results = rejourn.save_training(classes,content)
  return {'job_id':job.get_id()}

@app.route('/get_iobs', method=['OPTIONS','POST'])
def get_iob():
  request_type = request.json['request_type']
  content = request.json['content']
  classes = request.json['classes']
  class_legend = request.json['class_legend']
  pos_tags = request.json['pos_tags']
  if False:
    job = q.enqueue_call(
      func=rejourn.save_iob_training, 
      args=(request_type,class_legend, classes, pos_tags, content), 
      result_ttl=5000
    )
    return {'job_id':job.get_id()}
  else:
    results = rejourn.save_iob_training(request_type,class_legend, classes, pos_tags,content)
    return json.dumps(results)

@app.route('/assign_pos', method=['OPTIONS','POST'])
def assign_pos():
  content = request.json['content']
  results = rejourn.get_pos(content)
  return json.dumps(results)

@app.route('/entities', method=['OPTIONS','POST'])
def named_ent():
  content = request.json['content']
  results = rejourn.get_entities(content)
  return json.dumps(results)

@app.route("/results/:job_key",method=['GET'])
def get_results(job_key):
  sleep(2)
  try:
    job = Job.fetch(job_key, connection=conn)
    if job.is_finished:
      return json.dumps(job.result) 
    else:
      return "Nay!", 202
  except:
    return "Nay!", 202

app.install(EnableCors())

app.run(host='0.0.0.0', port=8080, debug=True)
