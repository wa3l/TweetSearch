#!/usr/bin/python

"""
TweetSearch.
Module: tweets_pr
Author: Wael Al-Sallami
"""

import prompt, timer

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
