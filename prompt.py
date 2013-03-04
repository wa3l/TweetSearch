#!/usr/bin/python

"""
Homework 2: Search Engine.
Module: prompt
Author: Wael Al-Sallami
Date: 2/10/2013
"""

import sys, re, cmd
import gen, engn, timer

class Prompt(cmd.Cmd):
  """Search query interface"""

  engine = None
  Index  = None
  # index_name = "mars_tweets_medium.json"
  index_name = "sample2.json"
  prompt = "\nquery> "
  welcome = "\n### Welcome to Wael's search engine!\n### Enter your query to perform a search.\n### Enter '?' for help and 'exit' to terminate."


  def preloop(self):
    """Print intro message and write or load indices"""
    print self.welcome
    with timer.Timer() as t:
      self.Index = gen.Index(self.index_name)
    print '> Request took %.03f sec.' % t.interval


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

