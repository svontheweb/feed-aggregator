from flask import Flask, render_template, jsonify, request, redirect, session, url_for
from flask_cors import CORS
import feedparser
from datetime import datetime, timedelta
from dateutil import tz
import requests
import youtube_handler
import db_utils as db
import time
import json
from flask_session import Session
import user_info as ui
import datetime
import pytz
import extraction
import diffbot


app = Flask(__name__)
CORS(app)

# Set the secret key to some random bytes.
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

@app.route('/rss_feed', methods=['POST'])
def rss_feed():
  url = request.form['rss_url']
  if youtube_handler.is_valid_youtube_url(url):
    channel_id = youtube_handler.get_channel_id(url)
    if channel_id is not None:
      url = youtube_handler.get_rss_feed_url(channel_id)
    else:
      return 'invalid youtube url'
  target_url = 'https://api.rss2json.com/v1/api.json?rss_url=' + url + '&api_key=lvc9yv9rghalgomqr5xlkojqlsu2ke8uwtwfzjj4&order_by=pubDate&order_dir=desc&count=40'
  response = requests.request("GET", target_url)
  print('code is: ', response.status_code)
  if (response.status_code != 200):
    return 'Sorry... the link you provided might be incorrect or there is some problem while connecting to it. \n Please re-try our service with a working url.'
  data = requests.get(target_url).json()

  articles = []
  for item in data['items']:
    article = {
      'title': item['title'],
      'description': item['description'][:700],
      'link': item['link'],
      'image_url': item['thumbnail']
    }
    pub_date = item['pubDate']
    # Convert pubDate from GMT to IST
    gmt_timezone = pytz.timezone('GMT')
    ist_timezone = pytz.timezone('Asia/Kolkata')  # Replace with the desired timezone
    pub_date_gmt = datetime.datetime.strptime(pub_date, '%Y-%m-%d %H:%M:%S')
    pub_date_ist = gmt_timezone.localize(pub_date_gmt).astimezone(ist_timezone)

    article['pubDate'] = pub_date_ist.strftime('%Y-%m-%d %H:%M:%S %Z%z')
    articles.append(article)
  # return jsonify(articles)
  return render_template('home.html', articles=articles, project_name = 'BuzzTracker')

@app.route('/article/<article_link>')
def article(article_link):
    # code to fetch article content using the article_link parameter
    # render the article template with the fetched content
    return 'were here'

# @app.route('/br')
# def br():
#   article_summary = request.args.get('article_summary')
#   url = "https://bionic-reading1.p.rapidapi.com/convert"
  
#   payload = {
#   	"content": article_summary,
#   	"response_type": "html",
#   	"request_type": "html",
#   	"fixation": "1",
#   	"saccade": "10"
#   }
#   headers = {
#   	"content-type": "application/x-www-form-urlencoded",
#   	"X-RapidAPI-Key": "add973eb1dmsh9e3d068cf9c9845p1041e0jsnd5f2097d70d4",
#   	"X-RapidAPI-Host": "bionic-reading1.p.rapidapi.com"
#   }
  
#   response = requests.post(url, data=payload, headers=headers)
#   content = response.content.decode('utf-8')
#   print(content)
#   return content      
@app.route('/br')
def br():
  article_link = request.args.get('article_link')
  full_text = diffbot.retrieve_full_text_using_link(article_link)
  return full_text

@app.route('/profile')
def profile():
  user_json = session.get('user')  # Retrieve the JSON object from the session
  if user_json:
    user = json.loads(user_json)  # Parse the JSON object back into a dictionary
    email = ui.get_loggedin_user_email()
    subbed_feeds = db.get_subbed_feeds(email)
    return render_template('profile.html', project_name = 'BuzzTracker', user_email=email, subbed_feeds = subbed_feeds)
  else:
    return "problem in profile"

@app.route('/submit_feed', methods=['POST'])
def submit_feed():
    
    email = ui.get_loggedin_user_email()
    feed_url = request.form.get('feedUrl')

    if email and feed_url:
        if db.save_subbed_feed_info(email, feed_url):
            return redirect(url_for('profile'))
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save to database'})
    else:
        return jsonify({'status': 'error', 'message': 'Invalid request data'})


@app.route("/my_feeds")
def my_feeds():
  articles = []
  email = ui.get_loggedin_user_email()
  subbed_feeds = db.get_subbed_feeds(email)
  # Extract domain names from subbed_feeds URLs
  domains = [extraction.extract_domain_name(url) for url in subbed_feeds]
  # return domains
  # Fetch articles from the database based on the domains
  articles = db.fetch_articles_by_domains(domains)
  # return articles
  article_count = len(articles)
  return render_template('my_feeds.html', project_name = 'BuzzTracker', articles=articles, article_count = article_count)


@app.route("/login")
def login():
  return render_template('login.html', project_name = 'BuzzTracker')

@app.route("/login_check", methods=['POST'])
def login_check():
  if request.method == 'POST':
    # Process the login form data
    email = request.form.get('email')
    password = request.form.get('password')
    # todo
    if db.if_email_exists(email) and db.if_password_matches(email, password):
      subbed_feeds = db.get_subbed_feeds(email)
      user = {
        "email": email,
        "subbed_feeds": subbed_feeds
      }
      json_object = json.dumps(user)
      session['user'] = json_object  # Store the JSON object in the session
      return redirect('/home')  # Redirect to the home page after successful login
    else:
        return "no such user in db"

@app.route("/signup")
def signup():
  return render_template('signup.html', project_name = 'BuzzTracker')

@app.route("/signup_check", methods=['POST'])
def signup_check():
  if request.method == 'POST':
    # Process the signup form data
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')
    if password == confirm_password:
      # Call your signup function to handle saving user information
      if not db.if_email_exists(email):
        db.save_user_info(email, password)
        return redirect('/login')  # Redirect to the home page after successful signup
      else:
        return "user already exists in our database"
    else:
      return "Passwords do not match"
  else:
    return render_template('signup.html')

@app.route('/logout')
def logout():
  # user_json = session.get('user')  # Retrieve the JSON object from the session
  # Remove the 'user_json' key from the session if it exists
  if 'user' in session:
    session.pop('user', None)
    return redirect('/')
  else:
    return "Problem logging you out"
    

@app.route("/home")
def home():
  user_json = session.get('user')  # Retrieve the JSON object from the session
  if user_json:
    user = json.loads(user_json)  # Parse the JSON object back into a dictionary
    return render_template('home.html', project_name = 'BuzzTracker')
  else:
    return "User not logged in"

@app.route("/")
def hello_world():
  return render_template('index.html', project_name = 'BuzzTracker')
  
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
