import const
from chunkers import ieer_chunked_sents, ClassifierChunker
from catchunked import CategorizedConllChunkCorpusReader as custom_reader
from nltk.corpus import treebank_chunk
import pickle
import nltk
import pdb


if False:
  ieer_chunks = list(ieer_chunked_sents())
  print("Writing new ieer_chunks.pickle")
  f = open('pickles/ieer_chunks.pickle','w+')
  pickle.dump(ieer_chunks,f)
  f.close()
else:
  f = open('pickles/ieer_chunks.pickle','r')
  ieer_chunks = pickle.load(f)
  f.close()

path = nltk.data.find('custom_corpora')
reader = custom_reader(path, r'entities.txt',
  const.ace_entities, cat_pattern=r'(.*)\.txt')
custom_doc = reader.chunked_sents()

aggregated_doc = ieer_chunks + custom_doc
chunker = ClassifierChunker(aggregated_doc)
print("Writing new entity.pickle")
f = open('pickles/entity.pickle','w')
pickle.dump(chunker,f)
f.close()
