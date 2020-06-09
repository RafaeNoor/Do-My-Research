import os
import json

import pandas as pd




from flask import Blueprint, render_template, session,abort, request
firebase_storage_file = Blueprint('firebase_storage_file',__name__)

BUCKET_NAME = "domyresearch-25720.appspot.com/o/"
@firebase_storage_file.route('/get_storage_urls/<string:phrase>/<path:url>')
def download_url_to_path(phrase,url):
    print("HELLOOOOOO")

    #TODO: Use flask argument parsing
    #args = obj.split(",")
    #phrase = args[0]
    #urls = args[1:]

    print("Phrase:\t",phrase)
    print("Urls:\t",url)
    csv_name = url.split("/")[-1]

    #url = url.split(BUCKET_NAME)[0]+BUCKET_NAME+url.split(BUCKET_NAME)[1].replace("/","%2F")
    #print("Formated URL:\t",url)
    print(request.args.get('alt'))
    alt = request.args.get('alt')
    token = request.args.get('token')

    url = url+"?"+"alt="+alt+"&token="+token
    url = url.split(BUCKET_NAME)[0]+BUCKET_NAME+url.split(BUCKET_NAME)[1].replace("/","%2F")

    print("Formated url:\t",url)

    if os.path.isfile(os.path.join('static',phrase,'csvs',csv_name)):
        print("Already exists")
        return {"msg":"file already exists"}

    if not os.path.isdir('static'):
        os.mkdir("static")

    if not os.path.isdir(os.path.join('static',phrase)):
        os.mkdir(os.path.join('static',phrase))

    if not os.path.isdir(os.path.join('static',phrase,'csvs')):
        os.mkdir(os.path.join('static',phrase,'csvs'))

    df = pd.read_csv(url)
    df.to_csv(os.path.join('static',phrase,'csvs',csv_name))




    print("Completed downloading csvs...")
    return {"msg":"Completed successfuly"}