
from flask import Flask
import time

from summarize import summarize_file
from google_search_term import google_search_file
from search_for_tweets import tweet_search_file
from firebase_storage import firebase_storage_file
from google_trend_analysis import google_trend_analysis_file

import os


app = Flask(__name__)
app.register_blueprint(summarize_file)
app.register_blueprint(google_search_file)
app.register_blueprint(tweet_search_file)
app.register_blueprint(firebase_storage_file)
app.register_blueprint(google_trend_analysis_file)

@app.route('/time')
def get_current_time():
    print(os.getenv('PUBLIC_URL'))
    return {'time':time.time()}

