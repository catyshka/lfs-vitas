# -*- coding: utf8 -*-
import os
import urllib2
import urllib
import json

def load_images(query, directory):
    #print 'query', query
    encoded_query = urllib.quote(query.encode('utf8'))#query.replace(' ', '%20')#urllib.urlencode(query)
    url = "http://ajax.googleapis.com/ajax/services/search/images?v=1.0&q=" + encoded_query
    c = urllib2.urlopen(url)
    page = c.read()
    print page
    jsonData = json.loads(page)
    for i, res in enumerate(jsonData['responseData']['results']):
        #print res
        img = res['url']
        index = img.rfind('.')
        ext = img[index:]
        image = urllib.URLopener()
        try:
            image.retrieve(img,directory + "/" + query.replace(' ', '_') + '_' + str(i) + '_' + res['width'] + 'x' + res['height'] + ext)
        except: 
            pass
#load_images('frap f4201', 'frap_F4201')


