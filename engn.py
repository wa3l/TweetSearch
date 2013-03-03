#!/usr/bin/python

"""
Homework 1: Search Engine.
Module: engn
Author: Wael Al-Sallami
Date: 2/10/2013
"""

import math
from collections import Counter

class Engine:
  """The search engine"""

  index = None
  query = []

  def __init__(self, index):
    """Save a pointer to our index"""
    self.index = index


  def search(self, query):
    """Perform any search and return answers"""
    self.query = query
    if not self.all_terms_present(): return

    scores = self.calculate_scores()
    # print scores
    # return self.top_50_answers(scores)


  def calculate_scores(self):
    """Calculate the document scores for the given query terms"""
    # qterms_weight = self.qterms_weight()
    qtf = self.query_terms_tf()
    qvector = self.get_vector(qtf)

    # scores = qlength = dlength = {}

    doc_vectors = []
    for t in self.query:
      # q_tf_idf = qterms_weight[t]
    #   for d in self.index.terms[t]:
    #     d_tf_idf = self.tf_idf(t, d)
    #     if d not in scores:
    #       scores[d] = qlength[d] = dlength[d] = 0.0
    #     scores[d]  += q_tf_idf * d_tf_idf
    #     qlength[d] += math.pow(q_tf_idf, 2)
    #     dlength[d] += math.pow(d_tf_idf, 2)

    # for d in scores:
    #   length = math.sqrt(qlength[d]) * math.sqrt(dlength[d])
    #   scores[d] /= length

    # return scores


  """optimize idfs"""
  def get_vector(self, counter):
    vector = []
    for k in self.index.terms:
      if counter[k] == 0: vector.append(0)
      else:
        tf  = 1 + math.log(counter[k], 2)
        idf = math.log(float(self.index.size)/len(self.index.terms[k]), 2)
        vector.append(tf * idf)
    return vector


  def all_terms_present(self):
    for t in self.query:
      if t not in self.index.terms: return False
    return True


  def top_50_answers(self, scores):
    """Sorts answer docs by their scores and returns the top 50"""
    answers = sorted(scores, key=lambda d: scores[d], reverse=True)
    return answers[0:50]


  def query_terms_tf(self):
    """Return a {'term': tf} dict for our query terms"""
    return Counter(self.query)


  def qterms_weight(self):
    """return a {'term': tf_idf} dict for our query terms """
    tfs = self.query_terms_tf()
    weights = {}
    for t in tfs:
      tf  = 1 + math.log(tfs[t], 2)
      idf = self.idf(t)
      weights[t] = tf * idf
    return weights


  def tf_idf(self, t, d):
    """return tf_idf for a document d and term t"""
    tf_idf = self.tf(t, d) * self.idf(t)
    return tf_idf


  def idf(self, t):
    """retrun idf of term t in the index"""
    return math.log(float(self.index.size)/len(self.index.terms[t]), 2)


  def tf(self, t, d):
    """return tf for term t in document d"""
    return 1 + math.log(self.index.terms[t][d]['tf'], 2)

