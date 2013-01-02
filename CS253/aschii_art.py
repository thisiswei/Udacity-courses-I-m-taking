
import webapp2 
import jinja2
import os
from google.appengine.ext import db
import urllib2
from xml.dom import minidom


template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)  

URL = 'http://api.hostip.info/?ip='
GMAPS_URL = "http://maps.googleapis.com/maps/api/staticmap?size=380x263&sensor=false&"


def get_coords(ip):
    url = URL + ip
    content = None
    try:
        content = urllib2.urlopen(url).read()
    except URLError:
        return
    if content:
        d = minidom.parseString(content)
        coords = d.getElementsByTagName("gml:coordinates")
        if coords and coords[0].childNodes[0].nodeValue:
            lon, lat = coords[0].childNodes[0].nodeValue.split(',')
            return db.GeoPt(lat, lon)

def gmaps_img(points):
    markers = '&'.join('markers=%s,%s' %(p.lat, p.lon)
                       for p in points)
    return  GMAPS_URL + markers



class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)
    coords = db.GeoPtProperty()

class BaseHandler(webapp2.RequestHandler): 
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)   
                 
    def render(self, template, **kw):
        self.response.write(self.render_str(template, **kw))    
    
    def write(self, *a, **kw):
        self.response.write(*a, **kw)


class MainHandler(BaseHandler):
    def render_ascii(self, title='', art='', error=''):
        arts = db.GqlQuery('select * from Art order by created DESC LIMIT 10')
        arts = list(arts)
        points = filter(None, (a.coords for a in arts))
        img_url = None
        if points:
            img_url = gmaps_img(points)
        self.render('asi.html', title = title, art = art, error = error, arts =
                   arts, img_url = img_url)

    def get(self):
        self.render_ascii()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')
        if title and art:
            a = Art(title = title, art = art)
            coords = get_coords(self.request.remote_addr)
            if coords:
                a.coords = coords
            a.put()
            self.redirect('/')
        else:
            error = 'wtf, both needed'
            self.render_ascii(title, art, error)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)   


