import webapp2 
import re
import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)  

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PW = re.compile(r"^.{3,20}$")
EMAIL = re.compile(r"^[\S]+@[\S]+\.[\S]+$")

def valid_username(username):
    return username and USER_RE.match(username)

def valid_password(password):
    return password and PW.match(password)

def valid_email(email):
    return not email or EMAIL.match(email)


def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.write(render_str(template, **kw))
    
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

class Rot13(BaseHandler):
    def get(self):
        self.render('rot13.html')
    
    def post(self):
        text = self.request.get('text')
        rot13 = ''
        if text:
            rot13 = text.encode('rot13')
        self.render('rot13.html', text=rot13)

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
            self.redirect('/welcome?username=' + username)

class Welcome(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('signup.html')





app = webapp2.WSGIApplication([
    ('/', Rot13),
    ('/signup', Signup),
    ('/welcome', Welcome)
], debug=True)   



