from flask import session
import json

def get_loggedin_user_email():
  user_json = session.get('user')  # Retrieve the JSON object from the session
  if user_json:
    user = json.loads(user_json)  # Parse the JSON object back into a dictionary
    email = user['email']
    return email
  else:
   return None

def get_loggedin_user_subbed_feeds():
  user_json = session.get('user')  # Retrieve the JSON object from the session
  if user_json:
    user = json.loads(user_json)  # Parse the JSON object back into a dictionary
    subbed_feeds = user['subbed_feeds']
    return subbed_feeds
  else:
   return None