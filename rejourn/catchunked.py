from nltk.corpus.reader import CategorizedCorpusReader, ConllCorpusReader, ConllChunkCorpusReader

class CategorizedConllChunkCorpusReader(CategorizedCorpusReader, ConllChunkCorpusReader):
  def __init__(self, *args, **kwargs):
    CategorizedCorpusReader.__init__(self, kwargs)
    ConllChunkCorpusReader.__init__(self, *args, **kwargs)

  def _resolve(self, fileids, categories):
    if fileids is not None and categories is not None:
      raise ValueError('Specify fileids or categories, not both')
    if categories is not None:
      return self.fileids(categories)
    else:
      return fileids

  def raw(self, fileids=None, categories=None):
    return ConllCorpusReader.raw(self, self._resolve(fileids,categories))

  def words(self, fileids=None, categories=None):
    return ConllCorpusReader.words(self, self._resolve(fileids, categories))
 
  def sents(self, fileids=None, categories=None):
    return ConllCorpusReader.sents(self, self._resolve(fileids, categories))

  def tagged_words(self, fileids=None, categories=None):
    return ConllCorpusReader.tagged_words(self, self._resolve(fileids, categories))
 
  def tagged_sents(self, fileids=None, categories=None):
    return ConllCorpusReader.tagged_sents(self, self._resolve(fileids, categories))

  def chunked_words(self, fileids=None, categories=None, chunk_types=None):
    return ConllCorpusReader.chunked_words(self, self._resolve(fileids, categories), chunk_types)

  def chunked_sents(self, fileids=None, categories=None, chunk_types=None):
    return ConllCorpusReader.chunked_sents(self, self._resolve(fileids, categories), chunk_types)

  def parsed_sents(self, fileids=None, categories=None, pos_in_tree=None):
    return ConllCorpusReader.parsed_sents(self, self._resolve(fileids, categories), pos_in_tree)

  def srl_spans(self, fileids=None, categories=None):
    return ConllCorpusReader.srl_spans(self, self._resolve(fileids, categories))

  def srl_instances(self, fileids=None, categories=None, pos_in_tree=None, flatten=True):
    return ConllCorpusReader.srl_instances(self, self._resolve(fileids, categories), pos_in_tree, flatten)

  def iob_words(self, fileids=None, categories=None, pos_in_tree=None):
    return ConllCorpusReader.iob_words(self, self._resolve(fileids, categories))

  def iob_sents(self, fileids=None, categories=None, pos_in_tree=None):
    return ConllCorpusReader.iob_sents(self, self._resolve(fileids, categories))
