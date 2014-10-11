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

article = """
The United States, as promised by President Obama, has stepped up its airstrike campaign in Iraq, hitting targets near Baghdad in the effort to help the Iraqi government win back territory seized by the Islamic State in Iraq and Syria, Pentagon officials said Monday.

The offensive is the first expansion of the United States campaign against the Islamist militant group that Mr. Obama outlined last week in a speech to the nation.
The new campaign included a strike on Monday southwest of Baghdad and one the day before near Sinjar, Iraq, the Defense Department said in a statement. The strikes, the Pentagon said, go beyond the United States' initial mission announced last month of 'protecting our own people and humanitarian missions.'

The strikes on Sunday and Monday involved both attack and fighter aircraft, which the Pentagon said destroyed six vehicles near Sinjar and an ISIS combat post that was firing on Iraqi troops. The United States has now carried out 162 airstrikes across Iraq to counter an ISIS offensive that quickly gained ground in northern Iraq and Syria and set up what the group said was an Islamic caliphate.

It was a small first step in what the president said last week would be a major and longstanding expansion of the military campaign against ISIS. That ambitious proposal includes American airstrikes in Syria and the deployment of 475 more military advisers to Iraq, bringing the total to 1,600.

Mr. Obama vowed that the United States did not intend to go it alone, and the administration said Sunday it had lined up support from Arab nations to help in the airstrike campaign, although officials would not say when that assistance would come or who would provide it.

Saudi Arabia has already agreed to provide a base to train Syrian fighters who oppose both ISIS and President Bashar al-Assad.

Mr. Obama announced the first airstrikes against ISIS in early August, when it appeared that the Kurdish capital, Erbil, would fall to the Islamists.

A version of this article appears in print on September 16, 2014, on page A11 of the New York edition with the headline: U.S. Airstrikes Hit Targets Near Baghdad Held by ISIS. 
"""
# split to sentences
# using punkt
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
article_sent = tokenizer.tokenize(article)

# tokenize words
word_tokenizer = TreebankWordTokenizer()
word_list = [word_tokenizer.tokenize(sent) for sent in article_sent]

# train pos tagger
# evaluate accuracy
test_sents = treebank.tagged_sents()[3000:]
test_chunks = treebank_chunk.chunked_sents()[3000:]
conll_test = conll2000.chunked_sents('test.txt')

train_new_tagger = False 
if train_new_tagger:
  train_sents = treebank.tagged_sents()[:3000]
  #create dictionary from treeback of most frequent words
  print("creating dictionary from treeback")
  model = word_tag_model(treebank.words(), treebank.tagged_words())
  
  #keeping tagger default for chaining purposes
  print("Training tagger")
  
  backoff= DefaultTagger('NN')
  nt = NamesTagger(backoff=backoff)
  #taggers = [UnigramTagger, BigramTagger, TrigramTagger]
  #trained_taggers = backoff_tagger(train_sents,taggers,backoff=nt)
  #Regexp - best to treat numbers? 
  regexp_tagger = RegexpTagger(patterns, backoff=nt)
  treebank_tagger = UnigramTagger(model=model,backoff=regexp_tagger)

  #skipping affix
  
  #skipping brill
  
  #TnT
  #Tried on 9/24 took a long time on evaluting accuracy
  #tagger = tnt.TnT(unk=backoff,Trained=True)
  #tagger.train(train_sents)

  #Used Classifier tagger because of accuracy. Could play around with cutoff probability for using
  #backoff tagger
  tagger = ClassifierBasedPOSTagger(train=train_sents,backoff=regexp_tagger,cutoff_prob=0.3)

  print("Writing new tagger.pickle")
  f = open('tagger.pickle','w')
  pickle.dump(tagger,f)
  f.close()
else:
  print("Opening existing tagger.pickle")
  f = open('tagger.pickle','r')
  tagger = pickle.load(f)

#Chunker
train_new_chunker = True
if train_new_chunker:
  train_chunks = treebank_chunk.chunked_sents()[:3000]
  conll_train= conll2000.chunked_sents('train.txt')
  #chunker = TagChunker(train_chunks)
  chunker = ClassifierChunker(conll_train)
else:
  #RegexpParser - pass trace=1 to get output
  chunker = RegexpParser(r'''
  NP:
    {(<DT>|<JJ>)<NN.*>+} #Noun Phrase - chunk
    }<VB.*>{ #Noun Phrase - chink
  PP:
    {<IN><VB.*>+}
    {<IN><NN.*>+}
  VP:{<VB.*>+<RP.*>+}
  ''')

#Tests for sequential backoff route
#print("tests should be true: " + str(tagger._taggers[-1]==backoff))
#print("tests should be true: " + str(isinstance(tagger._taggers[1],TrigramTagger)))


#Evaluate Accuracy of tagger
print("Skipping Accuracy")
#print("Evaluating Accuracy")
#print("Accuracy: " + str(tagger.evaluate(test_sents)))

#Evaluate Accuracy/Precision/Recall of Chunker
print("Evaluating Accuracy/Precision/Recall of Chunker")
score = chunker.evaluate(conll_test)
print("Accuracy: " + str(score.accuracy()))
print("Precision: " + str(score.precision()))
print("Recall: " + str(score.recall()))

# assign pos
tagged_sents = tagger.tag_sents(word_list)

# assign chunks
tagged_sents = [chunker.parse(tagged_sent) for tagged_sent in tagged_sents]
  
#From www.nltk.org/_modules/nltk/grammar.html pcfg_demo()
# import nltk.grammar as gram
# productions = []
# for tree in tagged_sents:
#   tree.collapse_unary(collapsePOS = False)
#   tree.chomsky_normal_form(horzMarkov = 2)
#   production += tree.productions()
# S = gram.Nonterminal('S')
# grammar = gram.induce_pcfg(S,productions)
# #This generates a grammar derived from the tagger and the trained chunker


# evaluate accuracy

#Output
for tree in tagged_sents:
  print(tree)


