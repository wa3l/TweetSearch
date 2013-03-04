#!/usr/bin/python

"""
Homework 2: Search Engine.
Module: part2
Author: Wael Al-Sallami
Date: 3/1/2013
"""

import prompt, gen, engn, timer

class PRUserSearch(prompt.Prompt):

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
    """Print results to the user"""
    if not users:
      print "\n> Error! No PageRanks were retrieved. :("
      return
    num = len(users)
    print "\n> Top %d users are:\n" % num
    for i in range(1, num+1):
      print "%s: %s" % (i, users[i-1])


def main():
  PRUserSearch().cmdloop()

if __name__ == '__main__':
  main()

