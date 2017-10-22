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
	
class State(ndb.Model):
	id = ndb.StringProperty(),
	state = ndb.StringProperty()


class MainPage(webapp2.RequestHandler):
	def get(self):
		state = hashlib.sha256(os.urandom(1024)).hexdigest()
		template_values = {
			'state' : state
		}
		
		new_key = State(id="", state=state)
		new_key.put()
		new_key.id = str(new_key.key.id())
		new_key.put()
		
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))
		
class OauthHandler(webapp2.RequestHandler):
	def get(self):
		self.response.write('Oauth')
	
class DisplayHandler(webapp2.RequestHandler):
	def post(self):
		self.response.write('DisplayHandler')


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/oauth', OauthHandler),
	('/display', DisplayHandler)
], debug=True)
# [END app}