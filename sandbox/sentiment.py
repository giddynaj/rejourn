import urllib2
from urllib2 import urlopen
import re
import cookielib
from cookielib import CookieJar
import time
import nltk
cj = CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
opener.addheader = [('User-agent','Mozilla/5.0')]


def processor(data):
    tokens = nltk.word_tokenize(data)
    tagged = nltk.pos_tag(tokens)     
    grammar = """ WHO: {<NN.+>:w
} """ 
    cp = nltk.RegexpParser(grammar)
    result = cp.parse(sentence)
    print(result)

def huffingtonRSSvisit():
    try:
        page = 'http://feeds.huffingtonpost.com/huffingtonpost/raw_feed'
        sourceCode = opener.open(page).read()
        try:
            links = re.findall(r'<link.*href=\"(.*?)\"', sourceCode)
            for link in links:
                if '.rdf' in link:
                    pass
                else:
                    print 'Visiting the link'
                    print '###########################'
                    linkSource = opener.open(link).read()
                    linesOfInterest = re.findall(r'<p>(.*?)</p>', str(linkSource))
                    print 'Content:'
                    for eachLine in linesOfInterest:
                        if '<img width' in eachLine:
                            pass
                        elif '<a href=' in eachLine;
                            pass
                        else:
                            print eachLine
        except Exception, e:
            print 'failed 2nd loop of huffingtonRSS'
            print str(e)
    except Exception, e:
        print str(e)

