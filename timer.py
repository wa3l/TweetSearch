#!/usr/bin/python

"""
TweetSearch.
Module: timer
Author: Wael Al-Sallami
"""

import time

class Timer:
  """Timer class used to profile different actions"""
  def __enter__(self):
    self.start = time.clock()
    return self

  def __exit__(self, *args):
    self.end = time.clock()
    self.interval = self.end - self.start
