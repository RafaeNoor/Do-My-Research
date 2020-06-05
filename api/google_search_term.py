from googleapiclient.discovery import build


SEARCH_API = "AIzaSyAeo1voHi9W8DvwWmmYWHLGdRiYEv7q1Gk"
CSE_ID = "004013468515777212927:zcb1rvnhyvq"

from flask import Blueprint, render_template, session,abort
google_search_file = Blueprint('google_search_file',__name__)

@google_search_file.route('/search/<string:search_term>')
def google_search(search_term, **kwargs):
    service = build("customsearch", "v1", developerKey=SEARCH_API)
    res = service.cse().list(q=search_term, cx=CSE_ID, **kwargs).execute()
    return res
