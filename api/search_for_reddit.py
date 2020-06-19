import requests

import json
from time import sleep

import pandas as pd
import numpy as np

from tensorflow.keras.preprocessing.sequence import pad_sequences
import tensorflow as tf
#from tensorflow.keras import backend

#backend.clear_session()

import os

from flask import Blueprint, render_template, session,abort
reddit_trend_analysis_file = Blueprint('reddit_trend_analysis_file',__name__)

from search_for_tweets import gender_detector, initialize_sentiment_classifier,preprocessing


from process_reddit_data import do_complete_analysis


def create_dir_for_phrase(phrase):
    if not os.path.isdir("static"):
        os.mkdir("static")

    if not os.path.isdir(os.path.join("static",phrase)):
        os.mkdir(os.path.join("static",phrase))

    if not os.path.isdir(os.path.join("static",phrase,"reddit")):
        os.mkdir(os.path.join("static",phrase,"reddit"))



    return os.path.join("static",phrase,"reddit")


fields = [
    "subreddit",
    "selftext",
    "author_fullname",
    "author",
    "title",
    "ups",
    "downs",
    "upvote_ratio",
    "url",
    "subreddit_subscribers",
]

sorts = [
    "new",
    "hot",
#    "relevance",
#    "top",
]

user_fields =  [
    "name",
    "link_karma",
    "comment_karma",
    "is_mod",
    "subreddit/title",
    "subreddit/public_description",
]

CYCLES = 1

def search_reddit(phrase,sort,cycles):
    results = []
    sleep_time = 3
    for c in range(0,cycles):
        while True:
            res = requests.get("http://www.reddit.com/search.json?q={}&sort={}&limit=25".format(phrase,sort))
            res_json = res.json()
            if "error" in res_json:
                print("[",sort,", cycle:",c,"]","Retrying...")
                sleep(sleep_time)
                sleep_time += 5
            else:
                break
        results.append(res_json)

    return results





#with open("read.json","r") as r:
#    res_json = json.load(r)

def filter_fields(ls_obj,keys):

    comb_df = []
    for obj_idx,obj in enumerate(ls_obj):
        children = obj["data"]["children"]

        other = []
        for idx,entry in enumerate(children):
            other.append({key: entry["data"][key] for key in keys})

        #other = get_all_users_info(other)

        df = pd.DataFrame.from_records(other)
        #df.to_csv("res_other.csv")

        if obj_idx == 0:
            comb_df = df
        else:
            comb_df = pd.concat([comb_df,df])

    #print(comb_df)

    return comb_df



@reddit_trend_analysis_file.route('/reddit_trend/<string:phrase>')
def get_reddit_posts(phrase):

    parent_dir = create_dir_for_phrase(phrase.replace(" ","_"))
    sent_classifier, tk_obj = initialize_sentiment_classifier()

    reddit_data = []

    print("Fetching posts...")
    for sort in sorts:
        reddit_data += search_reddit(phrase,sort,CYCLES)
        print("Done with SORT=",sort)

    df = filter_fields(reddit_data,fields)

    df = add_gender_and_sentiment(df,sent_classifier,tk_obj)

    df.to_csv(os.path.join(parent_dir,"{}_reddit.csv".format(phrase)))
    print(df)
    print("Done with fetching reddit posts")

    complete_analysis = do_complete_analysis(df,parent_dir,phrase)

    return {"analysis_obj":complete_analysis}



def add_gender_and_sentiment(df,sent_classifier,tk_obj):
    sentences = df[['title']]
    to_predict = preprocessing(sentences,'title')
    sequences_to_pred = tk_obj.texts_to_sequences(to_predict)
    to_predict_numeric=pad_sequences(sequences_to_pred,maxlen=200,padding='post')


    graph = tf.compat.v1.get_default_graph()#get_default_graph()
    #print(to_predict_numeric[19])

    #TODO: HACKish, add oov token instead
    for i in range(0,to_predict_numeric.shape[0]):
        for j in range(0,to_predict_numeric.shape[1]):
            if to_predict_numeric[i,j] >= 137252 :
                to_predict_numeric[i,j] = 0

    with graph.as_default():
        sentiments = sent_classifier.predict( to_predict_numeric ).tolist()
        sentiments = [np.argmax(sent) for sent in sentiments]

    df['sentiment'] = sentiments


    get_gender = lambda x: gender_detector.get_gender(x.split(" ")[0].lower())

    print()
    df['gender'] = df['author'].apply(get_gender)


    return df



def get_all_users_info(ls_obj):
    print("GETTING USER INFO")
    user_memo = {}

    names = [obj['author'] for obj in ls_obj]

    for idx,name in enumerate(names):
        print(idx)
        if name in user_memo:
            print("HIT")
            name_obj = user_memo[name]
        else:
            name_obj = get_user_info(name)
            user_memo[name] = name_obj

        for field in user_fields:
            true_field = field.split("/")[-1]
            ls_obj[idx][true_field] = name_obj[true_field]


    return ls_obj






def get_user_info(uuid):
    sleep_time = 2
    while True:
        res = requests.get("http://www.reddit.com/users/search.json?q={}".format(uuid))
        res_json = res.json()
        if "error" in res_json:
            sleep(sleep_time)
            sleep_time += 3
        else:
            break
    #print(res_json)
    #with open("check.json","w+") as w:
    #    w.write(json.dumps(res_json,indent=4))

    if res_json["data"]["dist"] < 1:
        print('empty')
        user_info = {key.split("/")[-1]: "" for key in user_fields}

    else:
        user_obj = res_json["data"]["children"][0]["data"]
        user_info = {}
        for field in user_fields:
            field_paths = field.split("/")
            item = user_obj
            for f in field_paths:
                item = item[f]
            user_info[field_paths[-1]] = item

    #print(user_info)
    return user_info





