import MySQLdb 
import pdb
from bs4 import BeautifulSoup
import nltk
import pdb

def processor(data):
    try:
        tokens = nltk.word_tokenize(data)
        tagged = nltk.pos_tag(tokens)
        grammar = """ Who: {<NN.+>}"""
        entities = nltk.chunk.ne_chunk(tagged)
        pdb.set_trace()
        print entities
    except Exception, e:
        print str(e)

try:
  db = MySQLdb.connect(host="localhost", # your host, usually localhost
                       user="root", # your username
                        passwd="root", # your password
                        db="mydb", charset='utf8') # name of the data base
  cur = db.cursor()
  
  sql = 'select content from news'
  cur.execute(sql)
  articles = [cur.fetchone()]
  for article in articles:
    article = article[0].encode('ascii','ignore')
    processor(article)
  
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
