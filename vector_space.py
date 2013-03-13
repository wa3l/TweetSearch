#!/usr/bin/python

"""
TweetSearch.
Module: vector_space
Author: Wael Al-Sallami
"""

import prompt, timer

class VSRSearch(prompt.Prompt):
  """Vector Retrieval search query interface"""

  def default(self, line):
    """Handle search query"""
    with timer.Timer() as t:
      answers = self.engine.search(self.parse_query(line))
      self.print_results(answers, line)
    print'\n> Search took %.06f sec.' % t.interval


def main():
  VSRSearch().cmdloop()

if __name__ == '__main__':
  main()

