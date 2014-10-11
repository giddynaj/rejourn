import nltk
from itertools import islice
from nltk.probability import *
productions = []
S = nltk.Nonterminal('S')
for tree in nltk.corpus.treebank.parsed_sents('wsj_0002.mrg'):
  productions += tree.productions()
grammar = nltk.induce_pcfg(S,productions)
print(grammar)
print nltk.FreqDist(productions).most_common(50)
parser = nltk.ChartParser(grammar)
for tree in parser.parse(productions):
  print(tree)

