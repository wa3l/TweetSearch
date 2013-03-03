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
from collections import Counter, namedtuple

class Index:
  """The data store"""
  size  = 0
  terms = {}
  docs  = {}
  users = {}
  pageranks = {}
  tweets = []
  index_name = "index.dat"


  def __init__(self, json_file):
    """Build index, store index"""
    if self.on_disk():
      print "\n> Reading index! This happens once per session, please wait ..."
      self.load()
    else:
      print "\n> Writing index! This only happens once, please wait ..."
      self.build(json_file)
      self.save()

    # for p in self.pageranks:
      # print str(self.users[p].name) + ": " + str(self.pageranks[p])


  def build(self, json_file):
    """Build index from tweets"""
    tweets = self.read_docs(json_file)
    self.size = len(tweets)
    for d in tweets:
      self.add_terms(d)
      self.add_doc(d)
      self.add_user(d.user)
      self.add_mentions(d)
    # self.pagerank()


  def pagerank(self, alpha=.85):
    tele = (1.0 - alpha) / len(self.users)
    # initialize pageranks
    prev_pr = dict.fromkeys(self.users, 1.0/len(self.users))
    next_pr = dict.fromkeys(self.users, 0)
    old = 0
    new = 0
    for u in prev_pr: old += prev_pr[u]
    for i in range(100):
      # conv = 0
      for u in self.users:
        for m in self.users[u].mentions:
          next_pr[m] += prev_pr[u]/len(self.users[u].mentions)

      # add teleportation:
      if i == 0:
        next_pr.update((k,v) for (k,v) in next_pr.iteritems() if v > 0)

      for u in next_pr:
        next_pr[u] = alpha * next_pr[u] + tele
        new += next_pr[u]
        # conv += abs(prev_pr[u] - next_pr[u])

      conv = abs(new - old)/len(next_pr)
      old = new
      new = 0
      print "i is %s and conv is %s" %(i, conv)
      if conv < 0.00001: break
      prev_pr = copy.deepcopy(next_pr)

    self.pageranks = next_pr


  def add_mentions(self, d):
    """Add all mentions to a user's adjacency list"""
    if not d.mentions: return
    User = namedtuple('User', ['id', 'name'])
    for m in d.mentions:
      if m['id'] == d.user.id: continue
      mentioned = User(m['id'], m['screen_name'])
      self.add_user(mentioned)
      self.users[d.user.id].mentions.add(mentioned.id)


  def add_user(self, user):
    """Add username to self.users[user-id]"""
    if user.id not in self.users:
      User = namedtuple('User', ['name', 'mentions'])
      self.users[user.id] = User(user.name, set())


  def add_terms(self, d):
    """Add all tweet tokens to our terms index"""
    counts = Counter(d.text)
    for t in counts:
      if t not in self.terms: self.terms[t] = {}
      self.terms[t][d.id] = counts[t]


  def add_doc(self, d):
    """Cache document to user relationships"""
    self.docs[d.id] = d.user.id


  def tokenize(self, text):
    """tokenize a tweet"""
    return re.split(r'[^\w]', text.lower(), flags=re.UNICODE)


  def read_docs(self, filename):
    """Read tweets into {'docID': text} dictionary"""
    f = open(filename, 'rU')
    Document = namedtuple('Document', ['id', 'text', 'user', 'mentions'])
    User     = namedtuple('User', ['id', 'name'])
    tweets = []
    for line in f:
      d = json.loads(line)
      tweet = Document(
        d['id'],
        self.tokenize(d['text']),
        User(d['user']['id'], d['user']['screen_name']),
        d['entities']['user_mentions']
      )
      tweets.append(tweet)
    f.close()
    return tweets


  def save(self):
    """Save index to disk"""
    return
    index_file = open(self.index_name, "w")
    index = {
      'terms':      self.terms,
      'pageranks':  self.pageranks,
      'users':      self.users,
      'docs':       self.docs
    }
    marshal.dump(index, index_file)
    del index
    index_file.close()


  def load(self):
    """Loads index into memory"""
    index_file = open(self.index_name)
    index = marshal.load(index_file)
    self.terms      = index['terms']
    self.pageranks  = index['pageranks']
    self.docs       = index['docs']
    self.users      = index['users']
    self.size       = len(index['docs'])
    del index
    index_file.close()


  def on_disk(self):
    """Return True if index is present on disk"""
    if os.path.exists(self.index_name): return True

