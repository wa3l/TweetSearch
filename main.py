#!/usr/bin/python

"""
Homework 1: Search Engine.
Module: main
Author: Wael Al-Sallami
Date: 2/10/2013
"""

import sys, re, cmd
import gen, engn, timer

class Prompt(cmd.Cmd):
  """Search query interface"""

  engine = None
  Index  = None
  prompt = "\nquery> "
  welcome = "\n### Welcome to Wael's search engine!\n### Enter your query to perform a search.\n### Enter '?' for help and 'exit' to terminate."


  def preloop(self):
    """Print intro message and write or load indices"""
    print self.welcome
    with timer.Timer() as t:
      self.Index = gen.Index("mars_tweets_medium.json")
    print '> Request took %.03f sec.' % t.interval


  def default(self, line):
    """Handle search query"""
    query = self.parse_query(line)
    if not self.engine: self.engine = engn.Engine(self.Index)

    with timer.Timer() as t:
      answers = self.engine.search(query)

    if answers:
      print "\n> Found %d search results:" % len(answers),
      for doc in answers: print doc,
      print ''
    else:
      print "\n> Sorry, your search for: (%s) did not yield any results :(" % line

    print'\n> Search took %.06f sec.' % t.interval


  def parse_query(self, line):
    """Parse the query into a list of terms"""
    return re.split(r'[^\w]', line.lower().strip(), flags=re.UNICODE)


  def emptyline(self):
    """Called when user doesn't enter anything"""
    print "\n> Enter your search query or type '?' for help."


  def do_exit(slef, line):
    """Type 'exit' to terminate the program"""
    return True


  def do_EOF(self, line):
    print '' # print new line for prettier exits
    return True


def main():
  Prompt().cmdloop()

if __name__ == '__main__':
  main()

