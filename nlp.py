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

# split to sentences
# using punkt
def sentence_tokenize(texts):
    sentence_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    article_sent = sentence_tokenizer.tokenize(texts)
    return article_sent

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


