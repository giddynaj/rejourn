import nltk.tag, nltk.chunk, itertools
from nltk.corpus import ieer
from nltk.tag import ClassifierBasedTagger
import nltk.data
import pdb

def chunk_trees2train_chunks(chunk_sents):
  tag_sents = [nltk.chunk.tree2conlltags(sent) for sent in chunk_sents]
  return [[((w,t),c) for (w,t,c) in sent] for sent in tag_sents]

def prev_next_pos_iob(tokens, index, history):
  word, pos = tokens[index]
  if index == 0:
    prevword, prevpos, previob = ('<START>',)*3
  else:
    prevword, prevpos = tokens[index-1]  
    previob = history[index-1]

  if index == len(tokens) - 1:
    nextword, nextpos = ('<END>',)*2
  else:
    nextword, nextpos = tokens[index+1]

  feats = {
    'word' : word,
    'pos'  : pos,
    'nextword' : nextword,
    'nextpos' : nextpos,
    'prevword' : prevword,
    'prevpos' : prevpos,
    'previob' : previob
  }
  return feats

def ieertree2conlltags(tree,tag=nltk.tag.pos_tag):
  words, ents = zip(*tree.pos())
  iobs = []
  prev = None
  
  for ent in ents:
    if ent == tree.label():
      iobs.append('O')
      prev = None
    elif prev == ent:
      iobs.append('I-%s' % ent)
    else:
      iobs.append('B-%s' % ent)
      prev = ent
  words, tags = zip(*tag(words))
  return itertools.izip(words, tags, iobs)
 
def ieer_chunked_sents(tag=nltk.tag.pos_tag):
  for doc in ieer.parsed_docs():
    tagged = ieertree2conlltags(doc.text, tag)
    yield nltk.chunk.conlltags2tree(tagged)

class ClassifierChunker(nltk.chunk.ChunkParserI):
  def __init__(self, train_sents, feature_detector=prev_next_pos_iob, **kwargs):
    if not feature_detector:
      feature_detector = self.feature_detector
    train_chunks = chunk_trees2train_chunks(train_sents)
    self.tagger = ClassifierBasedTagger(train=train_chunks, feature_detector=feature_detector, **kwargs)
  
  def parse(self,tagged_sent):
    if not tagged_sent: return None
    chunks = self.tagger.tag(tagged_sent)
    return nltk.chunk.conlltags2tree([(w,t,c) for ((w,t),c) in chunks])


