#!/usr/bin/python

"""
Homework 2: Search Engine.
Module: engn
Author: Wael Al-Sallami
Date: 3/1/2013
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
    return self.top_50_answers()


  def pagerank_search(self, query):
    self.query = query
    if not self.all_terms_present(): return
    docs  = self.matching_docs()
    ranks = self.index.pageranks
    docs  = sorted(docs, key=lambda d: ranks[self.index.docs[d]['user']], reverse=True)
    return docs[0:50]



  def calculate_scores(self):
    """Calculate the document scores for the given query terms"""
    self.calculate_idfs()
    docs     = self.matching_docs()
    terms    = self.all_terms_of(docs)
    query_tf = Counter(self.query)
    qvector  = self.query_vector(query_tf, terms)
    self.scores = {}
    for d in docs:
      self.scores[d] = self.cosim(qvector, self.doc_vector(d, terms))


  def cosim(self, q, d):
    """Return the Cosine Similarity score for a (q, d) vector pair"""
    dot_product = sum(i * j for i, j in zip(q, d))
    magnitude1  = math.sqrt(sum(n ** 2 for n in q))
    magnitude2  = math.sqrt(sum(n ** 2 for n in d))
    return dot_product / (magnitude1 * magnitude2)


  def doc_vector(self, doc, terms):
    """Build a document vector against terms set"""
    vector = []
    for t in terms:
      vector.append(self.weight(t, doc))
    return vector


  def query_vector(self, counter, terms):
    """Build a query vector based on query terms counter & terms set"""
    vector = []
    for t in terms:
      w = 0
      if counter[t] != 0:
        w = (1 + math.log(counter[t], 2)) * self.idf_weights[t]
      vector.append(w)
    return vector


  def matching_docs(self):
    """Return all documents that contain any of the query terms"""
    docs = []
    for t in self.query:
      docs.extend(self.index.terms[t].keys())
    return set(docs)


  def all_terms_of(self, docs):
    """Return all terms that occur in docs"""
    terms = []
    for d in docs: terms.extend(self.index.docs[d]['terms'])
    return set(terms)


  def all_terms_present(self):
    """Check if all query terms are in the index"""
    for t in self.query:
      if t not in self.index.terms: return False
    return True


  def top_50_answers(self):
    """Sorts answer docs by their scores and returns the top 50"""
    answers = sorted(self.scores, key=lambda d: self.scores[d], reverse=True)
    return answers[0:50]


  def top_50_users(self):
    """Return the top 50 ranked users"""
    ranks = self.index.pageranks
    users = sorted(ranks, key=lambda d: ranks[d], reverse=True)
    return [self.index.users[u]['name'] for u in users[0:50]]


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
    return 1 + math.log(self.index.terms[t][d], 2)
