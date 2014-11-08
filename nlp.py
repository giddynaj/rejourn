#!/usr/bin/python
# coding=utf-8
import nltk
import nltk.data
import string
import pdb
from nltk.tokenize import TreebankWordTokenizer
from nltk.tag import DefaultTagger
from nltk.tag import UnigramTagger, BigramTagger, TrigramTagger, RegexpTagger
#from nltk.tag import tnt
from nltk.tag.sequential import ClassifierBasedPOSTagger
from nltk.corpus import treebank, treebank_chunk, conll2000
from nltk.chunk import RegexpParser
from nltk.chunk.regexp import ChunkString, ChunkRule, ChinkRule
from tag_util import backoff_tagger, word_tag_model, patterns
from taggers import NamesTagger
from chunkers import ClassifierChunker
import pickle
import os, os.path

# split to sentences
# using punkt
def sentence_tokenize(texts):
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    article_sent = sentence_tokenizer.tokenize(texts)
    return article_sent

def receive_content(classes,texts):
    path = os.path.expanduser('~/nltk_data')
    b = open(path + '/custom_corpora/content_bad.txt','a')    
    g = open(path + '/custom_corpora/content_good.txt','a')    
    
    for id, text in enumerate(texts):
        if classes[id] == 1:
            b.write(text + '\n')
        else:
            g.write(text + '\n')

    b.close()
    g.close()

def add_training_text_to_sentence_tokenizer(text):
    import nltk.tokenize.punkt
    import codecs
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    text = codecs.open("sentence.txt","r","utf8").read()
    tokenizer.train(text)
    out = open("sentence.pickle","wb")
    pickle.dump(tokenizer, out)
    out.close()

#Stolen from http://stackoverflow.com/questions/21160310/training-data-format-for-nltk-punkt
def train_punktsent(trainfile, modelfile):
  """ Trains an unsupervised NLTK punkt sentence tokenizer. """
  punkt = PunktTrainer()
  try:
    with codecs.open(trainfile, 'r','utf8') as fin:
      punkt.train(fin.read(), finalize=False, verbose=False)
  except KeyboardInterrupt:
    print 'KeyboardInterrupt: Stopping the reading of the dump early!'
  ##HACK: Adds abbreviations from rb_tokenizer.
  abbrv_sent = " ".join([i.strip() for i in \
                         codecs.open('abbrev.lex','r','utf8').readlines()])
  abbrv_sent = "Start"+abbrv_sent+"End."
  punkt.train(abbrv_sent,finalize=False, verbose=False)
  # Finalize and outputs trained model.
  punkt.finalize_training(verbose=True)
  model = PunktSentenceTokenizer(punkt.get_params())
  with open(modelfile, mode='wb') as fout:
    pickle.dump(model, fout, protocol=pickle.HIGHEST_PROTOCOL)
  return model

# tokenize words
def word_tokenize(texts):
    word_tokenizer = TreebankWordTokenizer()
    word_list = [word_tokenizer.tokenize(sent) for sent in texts]
    return word_list

def get_pos_tagger():
    f = open('tagger.pickle','r')
    tagger = pickle.load(f)
    return tagger

def set_pos_tags(texts,pos_tagger):
    tagged_sents = pos_tagger.tag_sents(texts)
    return tagged_sents 

def get_chunk_tagger():
    f = open('chunk.pickle','r')
    tagger = pickle.load(f)
    return tagger

def set_chunk_tags(texts,chunk_tagger):
    tagged_sents = [chunk_tagger.parse(tagged_sent) for tagged_sent in texts]
    return tagged_sents

