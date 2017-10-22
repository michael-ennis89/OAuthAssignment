# Michael Ennis
# Oregon State University
# CS 496 Mobile Cloud and Software Development
# 10/22/2017
# Source: Using Jinja2 with google
# https://cloud.google.com/appengine/docs/standard/python/getting-started/generating-dynamic-content-templates
# Source: Hashlib
# https://docs.python.org/2.7/library/hashlib.html
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
import time

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
	
class State(ndb.Model):
	id = ndb.StringProperty(),
	state = ndb.StringProperty()

# [START MAINPAGE]
class MainPage(webapp2.RequestHandler):
	def get(self):
		# Create a state variable and set it in the template values object to pass to JINJA.
		state = hashlib.sha256(os.urandom(256)).hexdigest()
		template_values = {
			'state' : state
		}
		
		# Create new State object and store it in database.
		newkey = State(id="", state=state)
		newkey.put()
		newkey.id = str(newkey.key.id())
		newkey.put()
		
		# Display the index.html page with Jinja variables. 
		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))
# [END MAINPAGE]
		
# [START OauthHandler]
class OauthHandler(webapp2.RequestHandler):
	def get(self):
		# Request the state and code from webapp2
		state = self.request.get('state')
		code = self.request.get('code')
		verification = 0;
		
		#query to get a list of all the states.
		check_state = State.query()
		results = check_state.fetch()
		#find the state variable and delete it with the id set verification to true.
		for i in results:
			if (i.state == state):
				verification = 1
				ndb.Key("State", long(i.key.id())).delete()
				
		# If the state is found
		if (verification == 1):
			# My client id, secret, and redirec_uri
			client_id = "931042662040-5cc54gub0j7ds4o7tp3ehdq8b30cqo9s.apps.googleusercontent.com"
			client_secret = "Ok5k-VTZW1CfBLCeon9-PfYK"
			redirect_uri = "https://oauthdemoosu.appspot.com/oauth"
			
			# Load users code and my info into a payload to request the token. 
			payload = {
			'code' : code,
			'client_id' : client_id,
			'client_secret' : client_secret,
			'redirect_uri' : redirect_uri,
			'grant_type' : 'authorization_code'
			}
			
			# Request the token, store in JINJA2 template_values
			payload = urllib.urlencode(payload)
			tokenFetch = urlfetch.fetch(url="https://www.googleapis.com/oauth2/v4/token", payload = payload, method=urlfetch.POST)
			results = json.loads(tokenFetch.content)
			token = results['access_token']
			
			template_values = {
				'state' : state,
				'token' : token
			}

			# Display oauth.html page with JINJA variables
			template = JINJA_ENVIRONMENT.get_template('oauth.html')
			self.response.write(template.render(template_values))
		# Else display error bad request 
		else:
			self.response.write('400 Bad Request')
			self.response.set_status(400)
# [END OauthHandler]

# [START DisplayHandler]
class DisplayHandler(webapp2.RequestHandler):
	def post(self):
		# Request the state and code from webapp2
		state = self.request.get('state')
		token = self.request.get('token')
		
		# Set up the header string for requesting information.
		auth_header = 'Bearer ' + token
		
		headers = {
			'Authorization' : auth_header
		}
		
		# Request the profile information, store in json. 
		result = urlfetch.fetch(url="https://www.googleapis.com/plus/v1/people/me", headers = headers, method=urlfetch.GET)
		results = json.loads(result.content)
		
		# Check if user is a Google Plus user
		isPlusUser = results['isPlusUser']
		
		#If the user is a plus user, display information.
		if(isPlusUser):
			# Grab the required variables from the json and place in template.
			givenName = results['name']['givenName']
			familyName = results['name']['familyName']
			urls = results['url']
			
			template_values = {
				'firstName' : givenName,
				'lastName' : familyName,
				'url' : urls,
				'statevar' : state
			}
			
			template = JINJA_ENVIRONMENT.get_template('display.html')
			self.response.write(template.render(template_values))
		# Else display 400 Bad Request error
		else:
			self.response.write('400 Bad Request')
			self.response.set_status(400)
# [END DisplayHandler]
			
	


# [START app]
app = webapp2.WSGIApplication([
    ('/', MainPage),
	('/oauth', OauthHandler),
	('/display', DisplayHandler)
], debug=True)
# [END app}