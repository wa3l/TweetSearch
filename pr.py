#!/usr/bin/python
"""
TweetSearch.
Module: pr
Author: Wael Al-Sallami
"""

class PageRank:
  """Calculate PageRanks for Twitter users in the corpus"""
  users = {}

  def __init__(self, users):
    self.users = users


  def build(self, alpha=.9):
    """Build PageRanks for users graph"""
    prev = dict.fromkeys(self.users, 1.0/len(self.users))
    for i in range(100):
      new = self.aggregate_ranks(prev)
      if i == 0:
        new = self.remove_danglers(new)
      (new, diff) = self.teleport(new, prev, alpha)
      if diff < 0.0000001: break
      prev = new
    return new


  def aggregate_ranks(self, prev):
    """Aggregate ranks for each user"""
    new = dict.fromkeys(self.users, 0)
    for u in self.users:
      L = len(self.users[u]['mentions'])
      for m in self.users[u]['mentions']:
        new[m] += prev[u]/L
    return new


  def remove_danglers(self, ranks):
    """Remove dangling nodes from ranks"""
    ranks.update((k,v) for (k,v) in ranks.iteritems() if v > 0)
    return ranks


  def teleport(self, new, prev, alpha):
    """Add teleportation and calculate convergence"""
    tele = (1.0 - alpha) / float(len(self.users))
    diff = 0
    for u in new:
      new[u] = alpha * new[u] + tele
      diff += abs(prev[u] - new[u])
    return (new, diff)
