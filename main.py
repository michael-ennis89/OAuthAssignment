from google.appengine.ext import ndb
from datetime import datetime
import webapp2
import json
import jinja2


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