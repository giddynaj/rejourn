#!/usr/bin/python

import urllib2
import simplejson
import MySQLdb 
import pdb
import re
from bs4 import BeautifulSoup

google_feed_url = "http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=8&q=http%3A%2F%2Fnews.google.com%2Fnews%3Foutput%3Drss"

def getJsonFeed(url):
  try:
    req = urllib2.Request(url, None)
    opener = urllib2.build_opener()
    f = opener.open(req)
    feed = simplejson.load(f)
    return feed['responseData']['feed']['entries']
  except Exception, e:
    print str(e)

def getContentUrl(url):
  try:
    req = urllib2.Request(url, None)
    opener = urllib2.build_opener()
    f = opener.open(req)
    return f.read()
  except Exception, e:
    print str(e)


def putContentInDb(title, feed_source, news_source, content, link, cur):
  sql = 'insert into news(title, feed_source, news_source, content, link) values("%s", "%s", "%s", "%s", "%s");' % (entry['title'], 'google', news_source,  content, link)
  print sql
  cur.execute(sql)
  db.commit()
  print cur.fetchone()
    

db = MySQLdb.connect(host="localhost", # your host, usually localhost
                     user="root", # your username
                      passwd="root", # your password
                      db="mydb", charset='utf8') # name of the data base
cur = db.cursor()
try:
  
  google_feed = getJsonFeed(google_feed_url)
  for entry in google_feed:
    #Google Specific format
    news_source = re.split("-",entry['title'])[-1].strip()
    content_feed = BeautifulSoup(entry['content'])
    content_url = content_feed.find_all('a')[0].get('href').split('url=')[-1]
    content_raw = getContentUrl(content_url)
    if content_raw != None:
      content_clean = BeautifulSoup(content_raw)
      #[cc.extract() for cc in content_clean('a')]
      #[cc.extract() for cc in content_clean('script')]
      #[cc.extract() for cc in content_clean('noscript')]
      #[cc.extract() for cc in content_clean('style')]

      #content must be greater than 2 characters
      content_clean = [cc.get_text() for cc in content_clean('p') if len(cc.get_text()) > 2]

      #content must have punctuation at the end
      content_clean = [cc for cc in content_clean if bool(re.search(r'[.!?]$',cc))]

      #content must have more than two words
      content_clean = [cc for cc in content_clean if len(filter(None,cc.split(' '))) > 2]

      content_clean = ' '.join(content_clean)
      content_clean = content_clean.replace('"',"'")
      try:
        content_clean.decode('ascii')
      except UnicodeEncodeError, e:
        content_clean = re.sub(r'[^\x00-\x7F]+',' ', content_clean)

      putContentInDb(entry['title'], 'google', news_source, content_clean, content_url,cur)
  
except MySQLdb.Error, e:
  print "Error %d: %s" % (e.args[0], e.args[1])
  db.rollback()
  #sys.exit(1)

finally:
  if db:
    db.close()

