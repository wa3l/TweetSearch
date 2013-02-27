#!/usr/bin/python

"""
Homework 1: Search Engine.
Module: engn
Author: Wael Al-Sallami
Date: 2/10/2013
"""

import math

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
    for t in self.query:
      if t not in self.index.terms: return

    terms_tf_idf = self.query_terms_tf_idf()
    scores = self.calculate_scores(terms_tf_idf)
    return self.top_50_answers(scores)


  def calculate_scores(self, terms_tf_idf):
    """Calculate the document scores for the given query terms"""
    scores = qlength = dlength = {}
    for t in terms_tf_idf:
      q_tf_idf = terms_tf_idf[t]
      for d in self.index.terms[t]:
        d_tf_idf = self.tf_idf(t, d)
        if d not in scores:
          scores[d] = qlength[d] = dlength[d] = 0
        scores[d]  += q_tf_idf * d_tf_idf
        qlength[d] += math.pow(q_tf_idf, 2)
        dlength[d] += math.pow(d_tf_idf, 2)
        # length[d] += math.pow(d_tf_idf, 2)

    for d in scores:
      scores[d] /= math.sqrt(qlength[d]) * math.sqrt(dlength[d])

    return scores


  def top_50_answers(self, scores):
    """Sorts answer docs by their scores and returns the top 50"""
    answers = sorted(scores, key=lambda d: scores[d], reverse=True)
    return answers[0:50]


  def query_terms_tf(self):
    """Return a {'term': tf} dict for our query terms"""
    terms_tf = {}
    for t in self.query:
      if t not in terms_tf: terms_tf[t] = 0
      terms_tf[t] += 1
    return terms_tf


  def query_terms_tf_idf(self):
    """return a {'term': tf_idf} dict for our query terms """
    tfs = self.query_terms_tf()
    terms_tf_idf = {}
    for t in tfs:
      tf = math.log(tfs[t], 2) + 1
      terms_tf_idf[t] = tf * self.idf(t)
    return terms_tf_idf


  def tf_idf(self, t, d):
    """return tf_idf for a document pair on term t"""
    return self.tf(t, d) * self.idf(t)


  def idf(self, t):
    """retrun idf of term t in the index"""
    df = float(self.index.size)/len(self.index.terms[t])
    return math.log(df, 2)


  def tf(self, t, d):
    """return tf for term t in document d"""
    return 1 + math.log(self.index.terms[t][d], 2)

