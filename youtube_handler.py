import requests
import re

def is_valid_youtube_url(url):
  """
  Returns True if the given URL is a valid YouTube channel URL, False otherwise.
  """
  pattern1 = r'^https://www\.youtube\.com/channel/[a-zA-Z0-9_-]{24}$'
  # pattern2 = r'^https://www\.youtube\.com/([@#])?[a-zA-Z0-9_-]+$'
  pattern2 = r'^https://www\.youtube\.com/(@[a-zA-Z0-9_-]+)?(?:/(?:videos|shorts|about|channels|community|playlists|streams|featured))?$'

  return bool(re.match(pattern1, url) or re.match(pattern2, url))

def get_channel_id_from_url(url):
  """
  Extracts the channel ID from a valid YouTube channel URL and returns it as a string.
  Returns None if the URL is not valid.
  """
  if not is_valid_youtube_url(url):
      return None
  return url.split('/')[-1]

def get_rss_feed_url(channel_id):
  """
  Returns the RSS feed URL for a given YouTube channel ID as a string.
  """
  return f'https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}'



def get_channel_id(url):
  r = requests.get(url)
  if r.status_code != 200:
    return None
  pattern = r'{"key":"browse_id","value":"(.+?)"'
  match = re.search(pattern, r.text)
  if match:
    channel_id = match.group(1)
    print(channel_id)
    return(channel_id)
  else:
    return None
