import feedparser
import pprint
from pushbullet import Pushbullet



def send_pb_msg(title, msg):
    ACCESS_TOKEN = 'PUSHBULLET_ACCESS_TOKEN'

    pb = Pushbullet(ACCESS_TOKEN)
    push = pb.push_note(title, msg)

# Just some sample keywords to search for in the title
key_words = ['Malware', 'breach', 'leak', 'ransomware']

# get the urls we have seen prior
f = open('viewed_urls.txt', 'r')
urls = f.readlines()
urls = [url.rstrip() for url in urls] # remove the '\n' char
f.close()

def contains_wanted(in_str):
    # returns true if the in_str contains a keyword
    # we are interested in. Case-insensitive
    for wrd in key_words:
        if wrd.lower() in in_str:
            return True
    return False

def url_is_new(urlstr):
    # returns true if the url string does not exist 
    # in the list of strings extracted from the text file
    if urlstr in urls:
        return False
    else:
        return True

rss = 'https://cyware.com/rss'
feed = feedparser.parse(rss)
for key in feed["entries"]: 
    url = key['links'][0]['href']
    title = key['title']
    content = key['content']

    if contains_wanted(title.lower()) and url_is_new(url):
        print('{} - {}'.format(title, url))

        msgtitle = title
        msg = '{}\n{}'.format(title, url)

        send_pb_msg(msgtitle, msg)

        with open('viewed_urls.txt', 'a') as f:
            f.write('{}\n'.format(url))
