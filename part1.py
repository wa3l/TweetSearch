#!/usr/bin/python

"""
Homework 2: Search Engine.
Module: part1
Author: Wael Al-Sallami
Date: 2/10/2013
"""

import prompt, gen, engn, timer

class VectorRetriever(prompt.Prompt):
  """Search query interface"""

  def default(self, line):
    """Handle search query"""
    query = self.parse_query(line)
    if not self.engine: self.engine = engn.Engine(self.Index)

    with timer.Timer() as t:
      answers = self.engine.search(query)

    self.print_results(answers)
    print'\n> Search took %.06f sec.' % t.interval


  def print_results(self, answers):
    """Print results to the user"""
    if answers:
      print "\n> Found %d search results:" % len(answers),
      for doc in answers: print "%s," % doc,
      print ''
    else:
      print "\n> Sorry, your search for: (%s) did not yield any results :(" % line

def main():
  VectorRetriever().cmdloop()

if __name__ == '__main__':
  main()

