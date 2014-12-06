import bottle
from bottle import hook, post, run, get, route,  request, response
import json
import pdb
import rejourn


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
  return json.dumps(results)

@app.route('/tokenize_sent', method=['OPTIONS','POST'])
def tokenize_sent():
  content = request.json['content']
  results = rejourn.get_tokenized_sentences(content)
  return json.dumps(results)

@app.route('/get_sent', method=['OPTIONS','POST'])
def get_sent():
  content = request.json['content']
  classes = request.json['classes']
  results = rejourn.save_training(classes,content)
  return results

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
  job = Job.fetch(job_key, connection=conn)
  if job.is_finished:
    return "Yay", 200
  else:
    return "Nay!", 202

app.install(EnableCors())

app.run(host='0.0.0.0', port=8080, debug=True)
