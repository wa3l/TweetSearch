#!/usr/bin/python

"""
Homework 1: Search Engine.
Module: main
Author: Wael Al-Sallami
Date: 2/10/2013
"""

from __future__ import print_function
import sys, re, cmd
import gen, engn, timer

class Prompt(cmd.Cmd):
  """Search query interface"""

  engine = None
  store  = None
  prompt = "\nquery> "
  welcome = "\n### Welcome to Wael's search engine!\n### Enter your query to perform a search.\n### Enter '?' for help and 'exit' to terminate."


  def preloop(self):
    """Print intro message and write or load indices"""
    print(self.welcome)
    with timer.Timer() as t:
      self.store = gen.Store("books")
    print('> Request took %.03f sec.' % t.interval)


  def default(self, line):
    """Handle search query"""
    query = self.parse_query(line)
    if not self.engine: self.engine = engn.Engine(self.store)
    with timer.Timer() as t:
      answers = self.engine.search(query)

    if answers:
      print("\n> Found %d search results:" % len(answers), end=' ')
      for doc in answers: print(doc, end=' ')
      print()
    else:
      print("\n> Sorry, your search for: (%s) did not yield any results :(" % line)

    print('\n> Search took %.06f sec.' % t.interval)


  def parse_query(self, line):
    """Parse all three kinds of query terms into a dict"""
    query = {'bool': [], 'phrase': [], 'wild': []}
    line = re.sub(r'[_]|[^\w\s"*]', ' ', line.strip().lower())
    (query, line) = self.parse_wildcard(query, line)
    (query, line) = self.parse_phrase(query, line)
    (query, line) = self.parse_boolean(query, line)
    return query


  def parse_wildcard(self, query, line):
    """Extract wildcard queries into query{}"""
    wregex = r"([\w]+)?([\*])([\w]+)?"
    query['wild'] = re.findall(wregex, line)
    if query['wild']:
      line = re.sub(wregex, '', line)
      i = 0
      while i < len(query['wild']):
        query['wild'][i] = filter(len, query['wild'][i])
        i += 1
    return (query, line)


  def parse_phrase(self, query, line):
    """extract phrase query terms into query{}"""
    pregex = r'\w*"([^"]*)"'
    query['phrase'] = re.findall(pregex, line)
    if query['phrase']: line = re.sub(pregex, '', line)
    return (query, line)


  def parse_boolean(self, query, line):
    """ consider whatever is left as boolean query terms"""
    query['bool'] = line.split()
    return (query, line)


  def emptyline(self):
    """Called when user doesn't enter anything"""
    print("\n> Enter your search query or type '?' for help.")


  def do_exit(slef, line):
    """Type 'exit' to terminate the program"""
    return True


  def do_EOF(self, line):
    print() # print new line for prettier exits
    return True


def main():
  Prompt().cmdloop()

if __name__ == '__main__':
  main()








# {
#   "text":"Landing Might Be Just One of Mars Rover Curiosity\u2019s Hurdles [COMIC]: More About: Mars, NASA, trending http:\/\/t.co\/DpWG8tC0",
#   "created_at":"Mon Aug 06 02:31:35 +0000 2012",
#   "entities":{
#     "user_mentions":[],
#     "hashtags":[],
#     "urls":[{"indices":[102,122],"url":"http:\/\/t.co\/DpWG8tC0","expanded_url":"http:\/\/bit.ly\/RJwRC9","display_url":"bit.ly\/RJwRC9"}]
#   },
#   "user":{
#     "lang":"en",
#     "created_at":"Wed Jun 27 16:42:59 +0000 2012",
#     "statuses_count":3821,
#     "description":"sports and gaming fan, especially soccer.\r\n #ifollowback\r\n\u2592\u2592\u250c\u2565\u2565\u2510\u2592\u2588\u2580\u2588\u2580\u2588\u2592\u2580\u2588\u2580\u2580\u2588\u2592\u2588\u2580\u2588\u2592\u2592\u2588\u2592\u2580\u2588\u2580\u2588\u2592 \u2592\u2554\u2561\u2588\u2588\u255e\u255d\u2592\u2592\u2588\u2592\u2592\u2592\u2592\u2588\u2580\u2588\u2592\u2592\u2588\u2580\u2588\u2592\u2592\u2588\u2592\u2592\u2588\u2584\u2588\u2592 \u2592\u2592\u2514\u2565\u2565\u2518\u2592\u2592\u2584\u2588\u2584\u2592\u2592\u2584\u2588\u2584\u2592\u2592\u2584\u2588\u2584\u2588\u2592\u2584\u2588\u2592\u2584\u2588",
#     "friends_count":2176,
#     "url":"http:\/\/dld.bz\/earnmoneyblogging",
#     "profile_image_url_https":"https:\/\/si0.twimg.com\/profile_images\/2346416634\/pacman_ghost_icon_green_normal.png",
#     "followers_count":2151,"screen_name":"NeonGhost23","location":"","favourites_count":1,"verified":false,"id":620153104,"name":"\u2605NeonGhost\u2605"
#   },
#   "retweet_count":0,
#   "id":232302873797611521
# }
