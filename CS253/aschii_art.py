
import webapp2 
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)  



class Art(db.Model):
    title = db.StringProperty(required = True)
    art = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

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
        arts = db.GqlQuery('select * from Art order by created DESC')
        self.render('ascii.html', title = title, art = art, error = error, arts = arts)

    def get(self):
        self.render_ascii()

    def post(self):
        title = self.request.get('title')
        art = self.request.get('art')

        if title and art:
            a = Art(title = title, art = art)
            a.put()
            self.redirect('/')
        else:
            error = 'wtf, both needed'
            self.render_ascii(title, art, error)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)   

                   
