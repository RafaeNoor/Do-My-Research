from googleapiclient.discovery import build
import time


SEARCH_API ="AIzaSyC7QwPDs3kg4qazMDJG_U0iOZVIu_X8zJ0"
CSE_ID = '011475368195895382035:wtmoqhj0qbo'

ALT_CSE_ID = ['003215349188551669716:d6aoauzscsc', # INTELLEGNICA
              '011475368195895382035:wtmoqhj0qbo', # MOMINA
              '011475368195895382035:wtmoqhj0qbo', # RAFAE
              '004149351999943571432:keqev0m3uku', # JOHN DOE
              '003265273670318285103:uyfzphskgnm', # FARHAN
]

ALT_API = [
    "AIzaSyB6ht8hmslQpLppEHFIf2PzVLUoAgfixBU", # INTELLEGENCIA
    "AIzaSyC7QwPDs3kg4qazMDJG_U0iOZVIu_X8zJ0", # MOMINA
    "AIzaSyAeo1voHi9W8DvwWmmYWHLGdRiYEv7q1Gk", # RAFAE
    'AIzaSyDS1cPcyfcW1tf2FxN-NhI8faIBDyzsF9E', # JOHN DOE
    'AIzaSyDFy45-2HpTJ5EUDV5IHtJc5sOozS2xO3o', # FARHAN
]

KEY_INDEX = 0

SLEEP_TIME = 1



from flask import Blueprint, render_template, session,abort
google_search_file = Blueprint('google_search_file',__name__)

@google_search_file.route('/search/<string:search_term>')
def google_search(search_term, **kwargs):

    urls = []
    while True:
        try:
            global  KEY_INDEX
            SEARCH_API = ALT_API[KEY_INDEX]

            CSE_ID = ALT_CSE_ID[KEY_INDEX]
            service = build("customsearch", "v1", developerKey=SEARCH_API)
            res = service.cse().list(q=search_term, cx=CSE_ID,num=10, **kwargs).execute()
            items = res['items']
            urls = [item['link'] for item in items]
            print("Web Urls:\t",urls)
            break
        except:
            print("# Google Search API expired..., shifting to new key")
            KEY_INDEX = (KEY_INDEX+1) % len(ALT_CSE_ID)
            time.sleep(SLEEP_TIME)



    return urls


def google_search_images(search_term):
    urls = []
    while True:
        try:
            global  KEY_INDEX
            SEARCH_API = ALT_API[KEY_INDEX]

            CSE_ID = ALT_CSE_ID[KEY_INDEX]
            service = build("customsearch", "v1", developerKey=SEARCH_API)
            res = service.cse().list(q=search_term, cx=CSE_ID, num=10 ,searchType='image',fileType='png').execute()
            items = res['items']
            urls = [item['link'] for item in items]
            print('Image urls:\t',urls)
            break
        except:
            print("# Google Search API expired..., shifting to new key")
            KEY_INDEX = (KEY_INDEX+1) % len(ALT_CSE_ID)
            time.sleep(SLEEP_TIME)



    return urls


