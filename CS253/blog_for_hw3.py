import webapp2 
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)  

                               
#hw3 fro CS253

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str('post.html', p=self)

class BaseHandler(webapp2.RequestHandler): 
    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.response.write(self.render_str(template, **kw))    
    
    def write(self, *a, **kw):
        self.response.write(*a, **kw)


class BlogFront(BaseHandler): 
    def get(self):
        posts = db.GqlQuery('select * from Post order by created DESC') 
        self.render('blog_front.html', posts=posts)


class NewPost(BaseHandler):
    def get(self):
        self.render('new_post.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(subject = subject, content = content) 
            p.put()
            self.redirect('/blogs/'+str(p.key().id()))
        else:
            error = 'wtf, both needed'
            self.render('new_post.html', subject=subject, content=content, error=error) 

class PostPage(BaseHandler):
    def get(self, post_id):
        key = db.Key.from_path('Post', int(post_id))
        post = db.get(key)
        if not post:
            self.error(404)
            return
        self.render('post_id.html', post=post)

class MainHandler(BaseHandler):
    def get(self):
        self.response.write('wtf')

app = webapp2.WSGIApplication([
    ('/blogs', BlogFront),
    ('/blogs/newpost', NewPost),
    ('/blogs/([0-9]+)',PostPage)
], debug=True)   



