#!/usr/bin/python
# coding=utf-8
import string
import pdb
import os, os.path
from bs4 import BeautifulSoup as bs
from pygoogle import pygoogle as pg
import json
import urllib
import redis
 
def return_query(q):
    #g = pg(query)
    #g.pages = 6
    #results = g.search()
    #will exceed google service terms
    query = urllib.urlencode({'q' : q})
    url = 'http://ajax.googleapis.com/ajax/services/search/web?v=1.0&num=8&%s' % query
    search_response = urllib.urlopen(url)
    search_results = search_response.read()
    results = json.loads(search_results)
    data = results['responseData']['results']

    #path = os.path.expanduser('~/results')
    #b = open(path + '/google_results.html','r')    
    #results = b.read()
    #soup = bs(results)
    #link_dict = [{'title' : a.text, 'link' : a['href']} for a in soup('a') if a.has_attr('href')]
    link_dict = [{'title' : a['titleNoFormatting'], 'link' : a['url'], 'content' : a['content']} for a in data if a.has_key('url')]
    #b.close()
    return link_dict 

def receive_content(texts):
    path = os.path.expanduser('~/results')
    b = open(path + '/googleresults.txt','a')    
    b.write(str(texts))
    b.close()

def get_keys():
    r_server = redis.Redis("localhost") 
    return r_server.keys("*")

def get_tags(context_name):
    r_server = redis.Redis("localhost") 
    return r_server.smembers("tags:" + context_name)

def set_tags(context_name,tag_name):
    r_server = redis.Redis("localhost")
    return r_server.sadd("tags:" + context_name, tag_name)

def del_tags(context_name,tag_name):
    r_server = redis.Redis("localhost")
    return r_server.srem("tags:" + context_name, tag_name)

def get_hash(context_name):
    r_server = redis.Redis("localhost") 
    return r_server.hgetall("hash:" + context_name)

def set_hash(context_name,tag_name,value):
    r_server = redis.Redis("localhost")
    return r_server.hset("hash:" + context_name, tag_name, value)

def del_hash(context_name,tag_name):
    r_server = redis.Redis("localhost")
    return r_server.hdel("hash:" + context_name, tag_name)
