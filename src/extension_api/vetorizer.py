import os
import sys
from gensim import models
from gensim.models.doc2vec import LabeledSentence
from abc import ABCMeta

class Vectorizer(metaclass=ABCMeta):
    @abstractmethod
    def train(self):
      """学習を行う。コーパス作成など"""
      pass

class Doc2vec(Vectorizer):
  """テキストをベクトル化するもの。色んな手法が試せるように追加していく。"""
  def __init__(self):
    self.model = None

  def train(sentences):
    model = models.Doc2Vec(size=400, alpha=0.0015, sample=1e-4, min_count=1, workers=4)
    model.build_vocab(sentences)
    for x in range(30):
        print(x)
        model.train(sentences)
        ranks = []
        for doc_id in range(100):
            inferred_vector = model.infer_vector(sentences[doc_id].words)
            sims = model.docvecs.most_similar([inferred_vector], topn=len(model.docvecs))
            rank = [docid for docid, sim in sims].index(sentences[doc_id].tags[0])
            ranks.append(rank)
        print(collections.Counter(ranks))
        if collections.Counter(ranks)[0] >= PASSING_PRECISION:
            break
    return model