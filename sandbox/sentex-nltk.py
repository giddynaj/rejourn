import nltk
import re
import time

exampleArray = ["The incredibly intimidating NLP scares people away who are sissies"]

def processLanguage():
  try:
    for item in exampleArray:
      tokenized = nltk.word_tokenize(item)
      tagged = nltk.pos_tag(tokenized)
      print tagged

      chunkGram = r"""Chunk: {<RB\w?>*<VB\w?>*<NNP>} """
      chunkParser = nltk.RegexpParser(chunkGram)

      chunked = chunkParser.parse(tagged)
      print chunked

  except Exception, e:
    print str(e)


processLanguage()
