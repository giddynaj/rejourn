from nltk.tokenize import sent_tokenize
from bs4 import BeautifulSoup as bs
import nlp
import search as sear

def delete_tags(context,tag):
  q = sear.del_tags(context,tag)
  members = sear.get_tags(context)
  return {'results' : q, 'members' : list(members)}

def get_tags(keys, context):
  members = [""] 
  hmembers = [""]
  kmembers = [""] 
  if (keys == True):
    kmembers = sear.get_keys()
  else:
    members = list(sear.get_tags(context))
    hmembers = sear.get_hash(context)
  return {'members' : members, 'hmembers' : hmembers, 'kmembers' : kmembers}

def set_tags(tag,context):
  members = [""] 
  hmembers = [""]
  kmembers = [""] 
  
  if tag.find(":") > -1: 
    tag, value = tag.split(":")
    q = sear.set_hash(context,tag,value)
    hmembers = sear.get_hash(context) 
  else:
    q = sear.set_tags(context,tag)
    members = sear.get_tags(context) 
  return {'results' : q, 'members' : list(members), 'hmembers' : hmembers } 
  
def get_search(query):
  q = sear.return_query(query)
  {'results' : q} 

def get_tokenized_sentences(content):
  soup = bs(content)
  soup = soup.get_text()
  sent_tokenize_list = sent_tokenize(soup) 
  classes = [0 for sent in sent_tokenize_list]
  return {'class_legend' : { 0 : 'content', 1 : 'not-content' },'sentences' : sent_tokenize_list, 'classes' : classes}
  
def save_training(classes,content):
  nlp.receive_content(classes,content)
  return {'result' : 'success'}

def get_pos(content):
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
  return {'class_legend' : class_legend,'tokens' : tokens, 'classes' : classes}


def get_entities(content):
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
  return {'class_legend' : rne_dict,'tokens' : tokens, 'classes' : entities}
  
