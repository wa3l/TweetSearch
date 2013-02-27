#!/usr/bin/python

"""
Homework 1: Search Engine.
Module: gen
Author: Wael Al-Sallami
Date: 2/10/2013
"""

import os, re, gzip, timer, marshal, json

class Index:
  """The data store"""
  """
  Structure of index on disk:
  {
    'size' : number of tweets,
    'terms': {
      'term' : {
        'docsID': tf, ...
      },
      ...
    }
  }
  """
  size  = 0
  terms = {}
  docs  = {}
  index_name = "index.dat"


  def __init__(self, json_doc):
    """Build index, store index"""
    if self.on_disk():
      print "\n> Reading index! This happens once per session, please wait ..."
      self.load()
    else:
      print "\n> Writing index! This only happens once, please wait ..."
      self.read_docs(json_doc)
      self.build()
      self.save()


  def build(self):
    """Build index from tweets"""
    self.size = len(self.docs)
    for d in self.docs:
      tokens = self.tokenize(self.docs[d])
      for t in tokens: self.add_term(t, d)


  def add_term(self, t, d):
    """Add term t to terms collection and handle its data"""
    if t in self.terms:
      if d not in self.terms[t]:
        self.terms[t][d] = 0
      self.terms[t][d] += 1
    else:
      self.terms[t] = {d: 1}


  def tokenize(self, text):
    """tokenize a tweet"""
    return re.split(r'[^\w]', text.lower(), flags=re.UNICODE)


  def read_docs(self, filename):
    """Read tweets into {'docID': text} dictionary"""
    f = open(filename, 'rU')
    tweets = {}
    for line in f:
      doc = json.loads(line)
      self.docs[doc['id']] = doc['text']
    f.close()


  def save(self):
    """Save index to disk"""
    index_file = open(self.index_name, "w")
    index = {'size': self.size, 'terms': self.terms}
    marshal.dump(index, index_file)
    index_file.close()


  def load(self):
    """Loads index into memory"""
    index_file = open(self.index_name)
    index = marshal.load(index_file)
    self.terms = index['terms']
    self.size  = index['size']
    index_file.close()


  def on_disk(self):
    """Return True if index is present on disk"""
    if os.path.exists(self.index_name): return True

