#!/usr/bin/python

"""
Homework 2: Search Engine.
Module: prompt
Author: Wael Al-Sallami
Date: 3/1/2013
"""

import sys, re, cmd
import gen, engn, timer

class Prompt(cmd.Cmd):
  """Search query interface"""

  engine = None
  Index  = None
  index_name = "mars_tweets_medium.json"
  # index_name = "sample2.json"
  prompt = "\nquery> "
  welcome = "\n### Welcome to Wael's search engine!\n### Enter your query to perform a search.\n### Enter '?' for help and 'exit' to terminate."


  def preloop(self):
    """Print intro message and write or load indices"""
    print self.welcome
    self.load_engine()


  def parse_query(self, line):
    """Parse the query into a list of terms"""
    return re.split(r'[^\w]', line.lower().strip(), flags=re.UNICODE)


  def load_index(self):
    """Load the index into memory"""
    with timer.Timer() as t:
      self.Index = gen.Index(self.index_name)
    print '> Request took %.03f sec.' % t.interval


  def load_engine(self):
    """Instantiate the engine in memory"""
    self.load_index()
    if not self.engine:
      self.engine = engn.Engine(self.Index)


  def print_results(self, answers, line):
    """Print results to the user"""
    if not answers:
      print "\n> Sorry, your search for: (%s) did not yield any results :(" % line
      return
    num = len(answers)
    print "\n> Found %d search results:\n" % num,
    for i in range(1, num+1):
      print "%s: %s" % (i, answers[i-1])


  def emptyline(self):
    """Called when user doesn't enter anything"""
    print "\n> Enter your search query or type '?' for help."


  def do_exit(slef, line):
    """Type 'exit' to terminate the program"""
    return True


  def do_EOF(self, line):
    print '' # print new line for prettier exits
    return True
