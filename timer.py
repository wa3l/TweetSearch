#!/usr/bin/python

"""
Homework 2: Search Engine.
Module: timer
Author: Wael Al-Sallami
Date: 3/1/2013
"""

import time

class Timer:
  def __enter__(self):
    self.start = time.clock()
    return self

  def __exit__(self, *args):
    self.end = time.clock()
    self.interval = self.end - self.start
