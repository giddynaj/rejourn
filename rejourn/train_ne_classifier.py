from chunkers import ieer_chunked_sents, ClassifierChunker
from nltk.corpus import treebank_chunk
import pickle

ieer_chunks = list(ieer_chunked_sents())
chunker = ClassifierChunker(ieer_chunks[:80])
print("Writing new entity.pickle")
f = open('entity.pickle','w')
pickle.dump(chunker,f)
f.close()
