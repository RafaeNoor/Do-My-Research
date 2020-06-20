
from flask import Flask, request
import time

from summarize import summarize_file
from google_search_term import google_search_file
from search_for_tweets import tweet_search_file
from firebase_storage import firebase_storage_file
from google_trend_analysis import google_trend_analysis_file
from search_for_reddit import reddit_trend_analysis_file

import os


app = Flask(__name__,static_folder='../build', static_url_path='/')
app.register_blueprint(summarize_file)
app.register_blueprint(google_search_file)
app.register_blueprint(tweet_search_file)
app.register_blueprint(firebase_storage_file)
app.register_blueprint(google_trend_analysis_file)
app.register_blueprint(reddit_trend_analysis_file)

@app.route('/time')
def get_current_time():
    print(os.getenv('PUBLIC_URL'))
    return {'time':time.time()}

@app.route('/read_html/<html>')
def read_html(html):
    print(request.path)
    print("READ HTML invoked")
    print(html)
    #pdfkit.from_file('../public/index.html','static/out.pdf')

    return {"msg":"completed"}

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=int(os.environ.get('PORT',8080)))

