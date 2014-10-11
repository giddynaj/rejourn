from nltk.probability import FreqDist, ConditionalFreqDist
def backoff_tagger(train_sents, tagger_classes, backoff=None):
  try:
    for cls in tagger_classes:
      backoff = cls(train_sents, backoff=backoff)
    return backoff
  except Exception, e:
    print str(e)

def word_tag_model(words, tagged_words, limit=200):
  fd = FreqDist(words)
  most_freq = fd.keys()[:limit]
  cfd = ConditionalFreqDist(tagged_words)
  return dict((word, cfd[word].max()) for word in most_freq)


patterns = [
  (r'^\d+$','CD'),
]
