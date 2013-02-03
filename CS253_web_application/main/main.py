import webapp2 
import jinja2
import os
import hmac
import hashlib
import re
import random
import string
import json
from datetime import datetime, timedelta
from google.appengine.api import memcache
from google.appengine.ext import db




template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)  

SECRET = 'wtf'

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW = re.compile(r"^.{3,20}$")
EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PW.match(password)

def valid_email(email):
    return not email or EMAIL.match(email)


def make_salt():
    return ''.join(random.choice(string.letters) for _ in range(5))

def make_pw_hash(name, pw, salt = None):
    if not salt:
        salt = make_salt()
    h = hashlib.sha256(name + pw + salt).hexdigest()
    return '%s|%s' % (salt, h)   

def valid_pw(name, password, h):
    salt = h.split('|')[0]
    return h == make_pw_hash(name, password, salt)    

def make_secure_cookie(s):
    return '%s|%s' % (s, hmac.new(SECRET, s).hexdigest())

def check_secure_val(h):
    s = h.split('|')[0]
    return s if make_secure_cookie(s) == h else None

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class User(db.Model):
    name = db.StringProperty(required = True)
    pw_hash = db.StringProperty(required = True) 
    email = db.StringProperty()

    @classmethod
    def by_name(cls, name):
        u = User.all().filter("name = ", name).get()
        return u

    @classmethod
    def by_id(cls, uid):
        return cls.get_by_id(uid)

    @classmethod
    def register(cls, name, pw, email=None):
        pw_hash = make_pw_hash(name, pw)
        return cls(name=name, pw_hash=pw_hash, email=email)

    @classmethod
    def login(cls, name, pw):
        u = cls.by_name(name)
        if u and valid_pw(name, pw, u.pw_hash):
            return u  

class Post(db.Model):
    subject = db.StringProperty(required = True)
    content = db.TextProperty(required = True)
    created = db.DateTimeProperty(auto_now_add = True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return render_str('post.html', p=self)   

    def as_dict(self):
        time_fmt = '%c'
        d = {'subject': self.subject,
             'content': self.content,
             'created': self.created.strftime(time_fmt)}
        return d
        



class BaseHandler(webapp2.RequestHandler): 
    def render_str(self, template, **params):
        return render_str(template, **params)

    def render(self, template, **kw):
        self.response.write(self.render_str(template, **kw))  

    def render_json(self, d):
        json_text = json.dumps(d)
        self.response.headers['Content-Type'] = 'application/json; charset=UTF-8'
        self.write(json_text)

    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def set_secure_cookie(self, name, val):
        cookie_val = make_secure_cookie(val)
        self.response.headers.add_header(
            'Set-Cookie',
            '%s=%s; Path=/' % (name, cookie_val))
    
    def read_secure_cookie(self, name):
        cookie_val = self.request.cookies.get(name)
        return cookie_val and check_secure_val(cookie_val)

    def login(self, user):
        self.set_secure_cookie('user_id', str(user.key().id()))
    
    def logout(self):
        self.response.headers.add_header('Set-Cookie', "user_id=; Path=/")  



    def initialize(self, *a, **kw):
        webapp2.RequestHandler.initialize(self, *a, **kw)
        uid = self.read_secure_cookie('user_id')
        self.user = uid and User.by_id(int(uid))

        if self.request.url.endswith('.json'):
            self.format = 'json'
        else:
            self.format = 'html'





class Signup(BaseHandler):
    def get(self):
        self.render('signup.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')
        have_error = False
        errors = {}

        if not valid_username(username):
            have_error = True
            errors['error_username'] = 'wtf' 
        if not valid_password(password):
            have_error = True
            errors['error_password'] = 'invalid password'
        if password != verify:
            have_error = True
            errors['error_verify'] = 'password not match asshole'
        if not valid_email(email):
            have_error = True
            errors['error_email'] = 'invalid email, bitch' 
        if have_error:
            self.render('signup.html',**errors)
        else: 
            u = User.by_name(username) 
            if u:
                errors['error_username'] = 'user exist'
                self.render('signup.html', **errors) 
            else:
                u = User.register(username, password, email)
                u.put()
                self.login(u)
                self.redirect('/welcome')


class Login(BaseHandler):
    def get(self):
        self.render('login.html')

    def post(self):
        username = self.request.get('username')
        password = self.request.get('password')

        u = User.login(username, password)
        if u:
            self.login(u)
            self.redirect('/welcome')
        else:
            msg = 'Invalid'
            self.render('login.html', error=msg)



class Logout(BaseHandler):
    def get(self):
        self.logout()
        self.redirect('/signup')


class Uwelcome(BaseHandler):
    def get(self):
        if self.user:
            self.render('welcome.html', username = self.user.name)
        else:
            self.redirect('/signup')




class Welcome(BaseHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        visits = 0
        visit_cookie_val = self.request.cookies.get('visits')
        if visit_cookie_val:
            cookie_val = check_secure_val(visit_cookie_val)
            if cookie_val:
                visits = int(cookie_val)
        visits += 1
        new_cookie_val = make_secure_cookie(str(visits))
        self.response.headers.add_header('Set-Cookie', 'visits=%s' % new_cookie_val)
        
        if visits > 5:
            self.write('you are awesome')
        else:
            self.write('you been here %s times' % visits)

def time_set(key, val):
    save_time = datetime.utcnow()
    memcache.set(key, (val, save_time))

def time_get(key):
    r = memcache.get(key)
    if r :
        val, save_time = r
        age = (datetime.utcnow() - save_time).total_seconds()
    else:
        val,  age = None, 0
    return val, age

def add_post(post):
    post.put()
    get_posts(update = True)
    return str(post.key().id())

def get_posts(update = False):
    q = Post.all().order('-created').fetch(limit = 10)
    mc = 'BLOGS'
    posts, age = time_get(mc)
    if update or posts is None:
        posts = list(q)
        time_set(mc, posts)
    return posts, age

def time_str(age):
    s = 'Queried %s seconds ago'
    age = int(age)
    return s % age   

class BlogFront(BaseHandler): 
    def get(self):
        posts, age = get_posts()
        if self.format == 'html':
            self.render('blog_front.html', posts=posts, age = time_str(age))
        else:
            return self.render_json([p.as_dict() for p in posts])


class NewPost(BaseHandler):
    def get(self):
        self.render('new_post.html')

    def post(self):
        subject = self.request.get('subject')
        content = self.request.get('content')

        if subject and content:
            p = Post(subject = subject, content = content) 
            p.put()
            key = add_post(p)
            self.redirect('/blogs/'+key)
        else:
            error = 'wtf, both needed'
            self.render('new_post.html', subject=subject, content=content, error=error) 

class PostPage(BaseHandler):
    def get(self, post_id):
        post_key = 'POST_' + post_id
        post, age = time_get(post_key)
        if not post:
            key = db.Key.from_path('Post', int(post_id))
            post = db.get(key)
            time_set(post_key, post)
            age = 0
        if not post:
            self.error(404)
            return
        if self.format == 'html': 
            self.render('permalink.html', post=post, age = time_str(age))
        else:
            self.render_json(post.as_dict())



class Flush(BaseHandler):
    def get(self):
        get_posts(update=True)
        self.redirect('/blogs')


app = webapp2.WSGIApplication([ 
    ('/',Welcome),
    ('/blogs/signup', Signup),
    ('/welcome', Uwelcome),
    ('/blogs/login', Login),
    ('/blogs/logout', Logout),
    ('/blogs/?(?:\.json)?', BlogFront),
    ('/blogs/newpost', NewPost),
    ('/blogs/([0-9]+)(?:.json)?', PostPage),
    ('/blogs/flush', Flush)
], debug=True)   








