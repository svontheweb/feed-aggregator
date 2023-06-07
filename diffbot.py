import requests

# link = 'https%3A%2F%2Fwww.technologyreview.com%2F2020%2F09%2F04%2F1008156%2Fknowledge-graph-ai-reads-web-machine-learning-natural-language-processing%2F'
# link = 'https://www.livemint.com/news/india/netflix-disney-amazon-to-challenge-indias-tobacco-rules-for-streaming-11685714216171.html'
api_key = '563f90430f904475944bf38f898bad8e'
# url = "https://api.diffbot.com/v3/article?url={}&token={}".format(link, api_key)
headers = {"accept": "application/json"}
# response = requests.get(url, headers=headers)


def retrieve_full_text_using_link(link):
  link = link
  url = "https://api.diffbot.com/v3/article?url={}&token={}".format(link, api_key)
  response = requests.get(url, headers=headers)
  response_json = response.json()
  full_text = response_json['objects'][0]['text']
  BR_text = bionic_reading(full_text)
  return BR_text

def bionic_reading(text):
  url = "https://bionic-reading1.p.rapidapi.com/convert"
  
  payload = {
  	"content": text,
  	"response_type": "html",
  	"request_type": "html",
  	"fixation": "1",
  	"saccade": "10"
  }
  headers = {
  	"content-type": "application/x-www-form-urlencoded",
  	"X-RapidAPI-Key": "add973eb1dmsh9e3d068cf9c9845p1041e0jsnd5f2097d70d4",
  	"X-RapidAPI-Host": "bionic-reading1.p.rapidapi.com"
  }
  
  response = requests.post(url, data=payload, headers=headers)
  content = response.content.decode('utf-8')
  # print(content)
  return content 

if __name__ == '__main__':
  if response.status_code == 200:
    response_text = response.text
    response_json = response.json()

    pageUrl = response_json['request']['pageUrl']
    icon = response_json['objects'][0]['icon']
    title = response_json['objects'][0]['title']
    date = response_json['objects'][0]['date']
    article_text = response_json['objects'][0]['text']
    # Writing to file
    with open("diffbot_response.txt", "a") as file1:
        # Writing data to a file
        file1.write(icon + '\n' + title + '\n' + pageUrl + '\n' + date + '\n' + article_text + 
        '\n\n\n\n')

    print(icon)
    print(title)
    print(pageUrl)
    print(date)
    print(article_text)
else:
    print('error connecting to service')