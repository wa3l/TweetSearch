#!/usr/bin/python

"""
Homework : Search Engine.
Module: gen
Author: Wael Al-Sallami
Date: 3/1/2013

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
import os, re, gzip, timer, marshal, json, copy, pr
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
      print '\a'
    else:
      print "\n> Writing index! This only happens once, please wait ..."
      self.build(json_file)
      self.save()
      print '\a'


  def build(self, json_file):
    """Build index from tweets"""
    tweets = self.read_docs(json_file)
    self.size = len(tweets)
    for d in tweets:
      self.add_terms(d)
      self.add_doc(d)
      self.add_user(d['user'])
      self.add_mentions(d)
    self.pageranks = pr.PageRank(self.users).build()


  def add_terms(self, d):
    """Add all tweet tokens to our terms index"""
    for t in d['terms']:
      if t not in self.terms: self.terms[t] = {}
      self.terms[t][d['id']] = d['terms'][t]


  def add_doc(self, d):
    """Cache document to user relationships"""
    self.docs[d['id']] = {'user': d['user']['id'], 'terms': d['terms'].keys()}


  def add_user(self, user):
    """Add username to self.users[user-id]"""
    if user['id'] not in self.users:
      self.users[user['id']] = {'name': user['name'], 'mentions': set()}


  def add_mentions(self, d):
    """Add all mentions to a user's adjacency list"""
    if not d['mentions']: return
    user_id = d['user']['id']
    for m in d['mentions']:
      if m['id'] == user_id: continue
      self.add_user({'id': m['id'], 'name': m['screen_name']})
      self.users[user_id]['mentions'].add(m['id'])


  def tokenize(self, text):
    """tokenize a tweet"""
    return re.split(r'[^\w]', text.lower(), flags=re.UNICODE)


  def read_docs(self, filename):
    """Read tweets into {'docID': text} dictionary"""
    f = open(filename, 'rU')
    tweets = []
    for line in f:
      d = json.loads(line)
      tweet = {
              'id': d['id'],
           'terms': Counter(self.tokenize(d['text'])),
            'user': {'id': d['user']['id'], 'name': d['user']['screen_name']},
        'mentions': d['entities']['user_mentions']
      }
      tweets.append(tweet)
    f.close()
    return tweets


  def save(self):
    """Save index to disk"""
    # return
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

