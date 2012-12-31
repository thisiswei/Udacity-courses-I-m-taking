import webapp2


import jinja2
import os

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)  


months = ['January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']
          
def valid_month(month):
    m = dict((mon[:3].lower(), mon)
               for mon in months)
    return m.get(month[:3], None)

def valid_day(day):
    return int(day) if day.isdigit() and int(day) > 0 and int(day)<32 else None

def valid_year(year):
    if not year.isdigit(): return
    y = int(year)
    return y if (y>1900 and y<3000) else None


class MainHandler(webapp2.RequestHandler):
    def write_form(self, error='', month='', day='', year=''):
        t = jinja_env.get_template('index.html')
        self.response.write(t.render()%{'error': error,
                                        'month': month,
                                        'day': day,
                                        'year': year})
    def get(self):
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')
        
        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if (year and day and month):
            self.redirect('/thanks')
        else:
            self.write_form('wtf', user_month, user_day, user_year)

class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('yep')


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/thanks', ThanksHandler)
], debug=True)   

