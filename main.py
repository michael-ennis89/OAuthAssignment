from google.appengine.api import users
from google.appengine.ext import ndb
from datetime import datetime
import json
import os
import urllib
import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class MainPage(webapp2.RequestHandler):
	def get(self):
		self.response.write('Hello')
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render())
		
class OauthHandler(webapp2.RequestHandler):
	def get(self):
	
class DisplayHandler(webapp2.RequestHandler):
	def post(self):


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/oauth', OauthHandler),
	('/display', DisplayHandler)
], debug=True)
# [END app}