
from flask import Flask
import time

from summarize import summarize_file


app = Flask(__name__)
app.register_blueprint(summarize_file)

@app.route('/time')
def get_current_time():
    return {'time':time.time()}

