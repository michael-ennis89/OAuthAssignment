from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import urlfetch
from datetime import datetime
import json
import logging
import hashlib
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
		
		newkey = State(id="", state=state)
		newkey.put()
		newkey.id = str(newkey.key.id())
		newkey.put()
		
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))
		
class OauthHandler(webapp2.RequestHandler):
	def get(self):
		state = self.request.get('state')
		logging.info(state)
		code = self.request.get('code')
		verification = 0;
		
		check_state = State.query()
		results = qry.fetch()
		for i in results:
			if (i.state == state):
				verification = 1
				ndb.Key("State", long(i.key.id())).delete()
				
		if (verification == 1):
			client_id = "931042662040-5cc54gub0j7ds4o7tp3ehdq8b30cqo9s.apps.googleusercontent.com"
			clien_secret = "Ok5k-VTZW1CfBLCeon9-PfYK"
			redirect_uri = "https://oauthdemoosu.appspot.com/oauth"
			
			payload = {
			'code' : code,
			'client_id' : client_id,
			'clien_secret' : clien_secret,
			'redirect_uri' : redirect_uri,
			'grant_type' : 'authorization_code'
			}
			
			payload = urllib.urlencode(payload)
			results = urlfetch.fetch(url="https://www.googleapis.com/oauth2/v4/token", payload = payload, method=urlfetch.POST)
			
			time.sleep(0.5)
			results = json.loads(result.content)
			token = results['access_token']
			
			template_values = {
				'state' : state,
				'token' : token
			}

			template = JINJA_ENVIRONMENT.get_template('oauth.html')
			self.response.write(template.render(template_values))
		
		else:
			self.response.write('400 Bad Request')
			self.response.set_status(400)
	
class DisplayHandler(webapp2.RequestHandler):
	def post(self):
		state = self.request.get('state')
		token = self.request.get('token')
		
		auth_header = 'Bearer ' + token
		
		headers = {
			'Authorization' : auth_header
		}
		
		result = urlfetch.fetch(url="https://www.googleapis.com/plus/v1/people/me", headers = headers, method=urlfetch.GET)
		time.sleep(0.5)
		results = json.loads(result.content)
		
		isPlusUser = results['isPlusUser']
		
		if(isPlusUser):
			givenName = results['name']['givenName']
			familyName = results['name']['familyName']
			emails = results['emails']['value']
			
			template_values = {
				'firstName' : givenName,
				'lastName' : familyName,
				'emailAddress' : emails
			}
			
			template = JINJA_ENVIRONMENT.get_template('display.html')
			self.response.write(template.render(template_values))
		
		else:
			self.response.write('400 Bad Request')
			self.response.set_status(400)
			
	


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/oauth', OauthHandler),
	('/display', DisplayHandler)
], debug=True)
# [END app}