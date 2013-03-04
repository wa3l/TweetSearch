#!/usr/bin/python

"""
Homework 2: Search Engine.
Module: part3
Author: Wael Al-Sallami
Date: 3/1/2013
"""

import prompt, gen, engn, timer

class PRDocumentSearch(prompt.Prompt):
  """PageRanked Search query interface"""

  def default(self, line):
    """Handle search query"""
    query = self.parse_query(line)

    with timer.Timer() as t:
      answers = self.engine.pagerank_search(query)

    self.print_results(answers, line)
    print'\n> Search took %.06f sec.' % t.interval


def main():
  PRDocumentSearch().cmdloop()

if __name__ == '__main__':
  main()
