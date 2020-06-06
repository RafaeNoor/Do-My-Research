import subprocess as sb
import os,sys
import json
import pandas as pd
import glob

import random
import string
import time

import gender_guesser.detector as gender

import process_tweet_data as process

gender_detector = gender.Detector(case_sensitive=False)

random.seed(time.time())
i = 0

def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))



from flask import Blueprint, render_template, session,abort
tweet_search_file = Blueprint('tweet_search_file',__name__)

#CMD = "pip install searchtweets"
#sb.call(CMD,shell=True)


def create_dir_for_phrase(phrase):
    if not os.path.isdir("static"):
        os.mkdir("static")

    if not os.path.isdir(os.path.join("static",phrase)):
        os.mkdir(os.path.join("static",phrase))

    return os.path.join("static",phrase)


@tweet_search_file.route('/tweet_search/<string:phrase>')
def search_for_phrase(phrase):
    phrase = phrase.lower()
    dir_path = create_dir_for_phrase(phrase)

    file_name = os.path.join(dir_path,phrase)

    CMD = 'search_tweets.py --max-results 200 --results-per-call 100 --filter-rule "'+phrase+'" --filename-prefix '+file_name+"_"+randomString()+' --print-stream --credential-file twitter_api_info.yaml'
    print(CMD)
    try:
        #sb.call(CMD,shell=True)
        print("Hello")
    except:
        print("Used Up Quota")

    # Call process tweet on collected tweets
    objects = []
    files = glob.glob(dir_path+"/*.json")
    print(files)
    for file in files:
        with open(file,"r") as readFile:
            for line in readFile:
                objects.append(json.loads(line))


    #print(objects)
    df = produce_csv(objects,dir_path)
    #process.process_gender(df)
    file_paths = process.do_complete_analysis(df,dir_path,phrase)

    df = df[:10]
    print("Returning:",df)
    df = df.transpose()

    return {'data':df.to_dict(),
            'file_paths':file_paths}




# pretty print tweet objects
def jprint(obj):
    print("\n")
    print(json.dumps(obj,indent=4))

def get_user_info(user_obj):
    #print(user_obj['name'].split(" ")[0].lower())
    #print(gender_detector.get_gender(user_obj['name'].split(" ")[0].lower()))
    return {
        "user_id":user_obj['id'],
        "name": user_obj['name'],
        "screen_name": user_obj['screen_name'],
        "location": user_obj['location'],
        "verified": user_obj['verified'],
        "followers_count": user_obj['followers_count'],
        "friends_count": user_obj['friends_count'],
        "gender": gender_detector.get_gender(user_obj['name'].split(" ")[0].lower()),
    }





def handle_tweets(tweet):
    user_info = get_user_info(tweet['user'])
    user_info['text'] = tweet['text']
    if 'extended_tweet' in tweet:
        user_info['full_text'] = tweet['extended_tweet']['full_text']
    else:
        user_info['full_text'] = tweet['text']

    user_info['geo'] = tweet['geo']
    user_info['place'] = tweet['place']
    user_info['retweet_count'] =  tweet['retweet_count']
    user_info['reply_count'] =  tweet['reply_count']
    user_info['favorite_count'] =  tweet['favorite_count']

    user_info['type'] = 'regular'
    global i
    i = (i+1)%2
    user_info['sentiment'] = i

    pairs = {}
    if "retweeted_status" in tweet:
        user_info['type'] = 'retweet'
        pairs = handle_tweets(tweet['retweeted_status'])
    elif tweet['in_reply_to_status_id'] != "null":
        user_info['type'] = 'reply'

    pairs[tweet['id_str']] =  user_info




    return pairs




def produce_csv(obj,parent_dir):
    data = {}

    for tweet in obj:
        # Handle retweets
        results = handle_tweets(tweet) # possible recursive tweets, returns pairs of updates

        for k,v in results.items():
            data[k] = v

    #print(data)

    df = pd.DataFrame.from_dict(data)
    df = df.transpose()
    print(df)
    df.to_csv(os.path.join(parent_dir,'data_combine.csv'), index=False)
    return df




