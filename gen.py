#!/usr/bin/python

"""
Homework 1: Search Engine.
Module: gen
Author: Wael Al-Sallami
Date: 2/10/2013

# Structure of index on disk:
{
  'size' : number of tweets,
  'terms': {
    'term' : {
      'docsID': {'tf': 1, 'user': 32},
      'docsID': {'tf': 1, 'user': 31},
      ...
    },
    ...
  }
}
"""
import os, re, gzip, timer, marshal, json, copy
from collections import Counter

class Index:
  """The data store"""
  size  = 0
  terms = {}
  docs  = []
  users = {}
  mentions = {}
  pagerank = {}
  index_name = "index.dat"


  def __init__(self, json_file):
    """Build index, store index"""
    if self.on_disk():
      print "\n> Reading index! This happens once per session, please wait ..."
      self.load()
    else:
      print "\n> Writing index! This only happens once, please wait ..."
      self.read_docs(json_file)
      self.build()
      self.save()
    # for p in self.pagerank:
    #   print str(self.users[p]) + ": " + str(self.pagerank[p])


  def build(self):
    """Build index from tweets"""
    self.size = len(self.docs)
    for d in self.docs:
      self.add_terms(d)
      # self.add_user(d)
      # self.add_mentions(d)
    # self.pagerank()


  # def pagerank(self):
  #   alpha = 0.85
  #   tele = (1.0 - alpha) / len(self.users)
  #   # initialize pageranks
  #   prev_pr = dict.fromkeys(self.users, 1.0/len(self.users))
  #   next_pr = dict.fromkeys(self.users, 0)
  #   for i in range(100):
  #     conv = 0
  #     for u in self.mentions:
  #       for m in self.mentions[u]:
  #         next_pr[m] += prev_pr[u]/len(self.mentions[u])

  #     # add teleportation:
  #     if i == 0:
  #       next_pr.update((k,v) for (k,v) in next_pr.iteritems() if v > 0)

  #     for u in next_pr:
  #       next_pr[u] = alpha * next_pr[u] + tele
  #       conv += abs(prev_pr[u] - next_pr[u])

  #     if conv < 0.00001: break
  #     prev_pr = copy.deepcopy(next_pr)

  #   self.pagerank = next_pr


  def add_mentions(self, doc):
    """Add all mentions to a user's adjacency list"""
    if not doc['mentions']: return
    uid = doc['user']['id']
    if uid not in self.mentions:
      self.mentions[uid] = set()
    for m in doc['mentions']:
      if m['id'] == uid: continue
      self.users[m['id']] = m['screen_name']
      self.mentions[uid].add(m['id'])


  def add_user(self, doc):
    """Add username to self.users[user-id]"""
    uid = doc['user']['id']
    if uid not in self.users:
      self.users[uid] = doc['user']['name']


  def add_terms(self, d):
    """Add all tweet tokens to our terms index"""
    tokens = self.tokenize(d['text'])
    # for t in tokens: self.add_term(t, d)
    counts = Counter(tokens)
    for t in counts:
      if t not in self.terms: self.terms[t] = {}
      self.terms[t][d['id']] = counts[t]



  # def add_term(self, t, doc):
  #   """Add term t to terms collection and handle its data"""
  #   did = doc['id']
  #   uid = doc['user']['id']

  #   if t in self.terms:
  #     if did not in self.terms[t]:
  #       self.terms[t][did] = {'tf': 0, 'user': uid}
  #     self.terms[t][did]['tf'] += 1
  #   else:
  #     self.terms[t] = {did: {'tf': 1, 'user': uid}}


  def tokenize(self, text):
    """tokenize a tweet"""
    return re.split(r'[^\w]', text.lower(), flags=re.UNICODE)


  def read_docs(self, filename):
    """Read tweets into {'docID': text} dictionary"""
    f = open(filename, 'rU')
    tweets = {}
    for line in f:
      doc = json.loads(line)
      self.docs.append({
        'id':   doc['id'],
        'text': doc['text'],
        'user': {'id': doc['user']['id'], 'name': doc['user']['screen_name']},
        '@':    doc['entities']['user_mentions']
      })
    f.close()


  def save(self):
    """Save index to disk"""
    return
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

