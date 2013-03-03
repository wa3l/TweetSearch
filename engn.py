#!/usr/bin/python

"""
Homework 1: Search Engine.
Module: engn
Author: Wael Al-Sallami
Date: 2/10/2013
"""

import math, timer
from collections import Counter

class Engine:
  """The search engine"""
  index  = None
  query  = []
  scores = {}
  idf_weights = {}

  def __init__(self, index):
    """Save a pointer to our index"""
    self.index = index


  def search(self, query):
    """Perform any search and return answers"""
    self.query = query
    if not self.all_terms_present(): return
    self.calculate_scores()
    print self.scores
    return self.top_50_answers()


  def calculate_scores(self):
    """Calculate the document scores for the given query terms"""
    with timer.Timer() as t:
      self.calculate_idfs()
    print '> Request took %.03f sec.' % t.interval


    docs = set()
    for t in self.query:
      docs = docs.union(set(self.index.terms[t].keys()))

    terms = set()
    for d in docs:
      terms = terms.union(self.index.docs[d].terms)

    query_tf = Counter(self.query)
    qvector  = self.query_vector(query_tf, terms)

    self.scores = {}
    for d in docs:
      self.scores[d] = self.cosim(qvector, self.doc_vector(d, terms))
    return self.scores


  def cosim(self, q, d):
    """Return the Cosine Similarity score for a (q, d) vector pair"""
    dot_product = sum(i * j for i, j in zip(q, d))
    magnitude1  = math.sqrt(sum(n ** 2 for n in q))
    magnitude2  = math.sqrt(sum(n ** 2 for n in d))
    return dot_product / (magnitude1 * magnitude2)


  def doc_vector(self, doc, terms):
    vector = []
    for t in terms:
      vector.append(self.weight(t, doc))
    return vector


  """optimize idfs"""
  def query_vector(self, counter, terms):
    vector = []
    for t in terms:
      w = 0
      if counter[t] != 0:
        w = (1 + math.log(counter[t], 2)) * self.idf_weights[t]
      vector.append(w)
    return vector


  def all_terms_present(self):
    for t in self.query:
      if t not in self.index.terms: return False
    return True


  def top_50_answers(self):
    """Sorts answer docs by their scores and returns the top 50"""
    answers = sorted(self.scores, key=lambda d: self.scores[d], reverse=True)
    return answers[0:50]


  def calculate_idfs(self):
    """Cache IDF weights for all terms"""
    if self.idf_weights: return
    for t in self.index.terms:
      self.idf_weights[t] = self.idf(t)


  def weight(self, t, d):
    """return tf_idf weight for a document d and term t"""
    weight = 0
    if d in self.index.terms[t]:
      weight = self.tf(t, d) * self.idf_weights[t]
    return weight


  def idf(self, t):
    """retrun idf of term t in the index"""
    return math.log(float(self.index.size)/len(self.index.terms[t]), 2)


  def tf(self, t, d):
    """return tf for term t in document d"""
    # return 1 + math.log(self.index.terms[t][d]['tf'], 2)
    return 1 + math.log(self.index.terms[t][d], 2)


