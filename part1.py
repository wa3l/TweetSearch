#!/usr/bin/python

"""
Homework 2: Search Engine.
Module: part1
Author: Wael Al-Sallami
Date: 3/1/2013
"""

import prompt, gen, engn, timer

class VSRSearch(prompt.Prompt):
  """Vector Retrieval search query interface"""

  def default(self, line):
    """Handle search query"""
    with timer.Timer() as t:
      answers = self.engine.search(self.parse_query(line))
    self.print_results(answers, line)
    print'\n> Search took %.06f sec.' % t.interval
    index = self.engine.index


def main():
  VSRSearch().cmdloop()

if __name__ == '__main__':
  main()

