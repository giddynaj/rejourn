import urllib2
import simplejson
import MySQLdb 
import pdb
from bs4 import BeautifulSoup

req = urllib2.Request("http://ajax.googleapis.com/ajax/services/feed/load?v=1.0&num=8&q=http%3A%2F%2Fnews.google.com%2Fnews%3Foutput%3Drss", None)
opener = urllib2.build_opener()
f = opener.open(req)
feed = simplejson.load(f)

print len(feed['responseData']['feed']['entries'])
print [entry['title'] for entry in feed['responseData']['feed']['entries']]

try:
  db = MySQLdb.connect(host="localhost", # your host, usually localhost
                       user="root", # your username
                        passwd="root", # your password
                        db="mydb", charset='utf8') # name of the data base
  cur = db.cursor()
  
  for entry in feed['responseData']['feed']['entries']:
    print entry['title']
    content_html = BeautifulSoup(entry['content'])
    content_clean = content_html.get_text()
    content_clean = content_clean.replace('"',"'")
    sql = 'insert into news(title, source, content) values("%s", "%s", "%s");' % (entry['title'], 'google', content_clean)
    print sql
    cur.execute(sql)
    db.commit()
    print cur.fetchone()
  
except MySQLdb.Error, e:
  print "Error %d: %s" % (e.args[0], e.args[1])
  db.rollback()
  #sys.exit(1)

finally:
  if db:
    db.close()
# feed is a dict type
#store this in mysql or some file
#execute this in cli use execfile('{filename with py}')
