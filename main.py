import pytumblr
import uuid
import json
import web
import collections
from keyring import *
from pprint import pprint as pp

BLOG = 'adventuring-co.tumblr.com'

client = pytumblr.TumblrRestClient(
    keys[0],
    keys[1],
    keys[2],
    keys[3],
)

pWhole = client.posts(BLOG, tag='portfolio')

URLS = (
    '/'     , 'index',
    '/feed' , 'feed' ,
)

class index:
    def GET(self):
        out = 'a'
        try:
            f = open('index.html')
            out = f.read() 
            f.close()
        except:
            out = "Failed to load templates"
        return out
 
class feed:
    def GET(self):
        GALLERY = {}
        out = ''
        for i in pWhole['posts']:
            order = filter(lambda x: 'order' in x, i['tags'])[0].replace('order-','')
            gItm = order + '-' + str(uuid.uuid1())
            GALLERY[gItm] = {}
            GALLERY[gItm]['order']  = str(order)
            GALLERY[gItm]['url']    = i['photos'][0]['original_size']['url']
            GALLERY[gItm]['width']  = i['photos'][0]['original_size']['width']
            GALLERY[gItm]['height'] = i['photos'][0]['original_size']['height']
        out = json.dumps(GALLERY, sort_keys=True, indent=4, separators=(',', ': '))

        return out

if __name__ == "__main__":
    app = web.application(URLS, globals())
    app.run()
