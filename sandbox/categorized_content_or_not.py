#From 1491 of cookbook
#This is how we would load in the customized corpus
from nltk.corpus.reader import CategorizedPlaintextCorpusReader
#reader = CategorizedPlaintextCorpusReader('.',r'movie_.*\.txt', cat_pattern=r'movie_(\w+)\.txt')
#reader = CategorizedPlaintextCorpusReader('.',r'movie_.*\.txt', cat_map={'movie_pos.txt':['pos'],'movie_next.txt':['neg']})
reader = CategorizedPlaintextCorpusReader('./nltk_data/custom_corpora/',r'content_.*\.txt', cat_map={'content_good.txt':['good'],'content_bad.txt':['bad']})

reader.categories()
#['neg','pos']
reader.fileids(categories=['good'])
#['movie_neg.txt']
reader.fileids(categories=['bad'])
#['movie_pos.txt']

#location 3442
#extract features from the corpus

def bag_of_words(words):
  return dict([(word, True) for word in words])

def bag_of_words_not_in_set(words, badwords):
  return bag_of_words(set(words) - set(badwords))

from nltk.corpus import stopwords
def bag_of_non_stopwords(words, stopfile='english'):
  badwords = stopwords.words(stopfile)
  return bag_of_words_not_in_set(words, badwords)

from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures

def bag_of_bigrams_words(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
  bigram_finder = BigramCollocationFinder.from_words(words)
  bigrams = bigram_finder.nbest(score_fn, n)
  return bag_of_words(words + bigrams)

#3529
import collections
def label_feats_from_corpus(corp, feature_detector=bag_of_words):
  label_feats = collections.defaultdict(list)
  for label in corp.categories():
    for fileid in corp.fileids(categories=[label]):
      feats = feature_detector(corp.words(fileids=[fileid]))
      label_feats[label].append(feats)
  return label_feats

def split_label_feats(lfeats, split=0.75):
  train_feats = []
  test_feats = []
  for label, feats in lfeats.iteritems():
    cutoff = int(len(feats) * split)
    train_feats.extend([(feat,label) for feat in feats[:cutoff]])
    test_feats.extend([(feat,label) for feat in feats[cutoff:]])
  return train_feats, test_feats

#Training NaiveBayesClassifier
from nltk.corpus import movie_reviews
cfeats = label_feats_from_corpus(reader)
mfeats = label_feats_from_corpus(movie_reviews)
#lfeats.keys()
##['neg','pos']
#train_feats, test_feats = split_label_feats(lfeats)

#from nltk.classify import NaiveBayesClassifier
#nb_classifier = NaiveBayesClassifier.train(train_feats)

