#!/usr/bin/python

"""
TweetSearch.
Module: prompt
Author: Wael Al-Sallami
"""

import sys, re, cmd, gen, engn, timer

class Prompt(cmd.Cmd):
  """Search query interface"""

  engine     = None
  Index      = None
  index_name = "mars_tweets_medium.json"
  prompt     = "\nquery> "
  welcome    = "\n### Welcome to Wael's search engine!\n### Enter your query to perform a search.\n### Enter '?' for help and 'exit' to terminate."


  def preloop(self):
    """Print intro message and write or load indices"""
    print self.welcome
    self.load_engine()


  def parse_query(self, line):
    """Parse the query into a list of terms"""
    return re.split(r'[^\w]', line.lower().strip(), flags=re.UNICODE)


  def load_engine(self):
    """Instantiate the engine & index in memory"""
    with timer.Timer() as t:
      if not self.engine:
        self.engine = engn.Engine(gen.Index(self.index_name))
    print '> Request took %.03f sec.' % t.interval


  def print_results(self, answers, line):
    """Print results to the user"""
    if not answers:
      print "\n> Sorry, your search for: (%s) did not yield any results :(" % line
      return
    print "\n> Found %d search results:\n" % len(answers),
    for i in range(len(answers)):
      print "%s: %s" % (i+1, answers[i])


  def emptyline(self):
    """Called when user doesn't enter anything"""
    print "\n> Enter your search query or type '?' for help."


  def do_exit(slef, line):
    """Type 'exit' to terminate the program"""
    return True


  def do_EOF(self, line):
    print '' # print new line for prettier exits
    return True
