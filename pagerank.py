#!/usr/bin/python

"""
TweetSearch.
Module: pagerank
Author: Wael Al-Sallami
"""

import prompt, timer

class PRUserSearch(prompt.Prompt):
  """PageRanked Users interface"""

  def preloop(self):
    """Print intro message and write or load indices"""
    print self.welcome
    self.load_engine()

    with timer.Timer() as t:
      users = self.engine.top_50_users()
      self.print_results(users)

    print'\n> Ranking took %.06f sec.' % t.interval
    exit()


  def print_results(self, users):
    """Overloaded: Print results to the user"""
    if not users:
      print "\n> Error! No PageRanks were retrieved. :("
      return
    print "\n> Top %d users are:\n" % len(users)
    for i in range(len(users)):
      print "%s: %s" % (i+1, users[i])


def main():
  PRUserSearch().cmdloop()

if __name__ == '__main__':
  main()

