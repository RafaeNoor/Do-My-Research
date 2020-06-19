import os,sys
import json
import pandas as pd
import glob

import random
import string
import time

import gender_guesser.detector as gender

import process_tweet_data as process
from nltk.stem.wordnet import WordNetLemmatizer
import pickle

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense, LSTM, Dropout

from keras.layers.embeddings import Embedding
from tensorflow.keras.preprocessing.sequence import pad_sequences

from tensorflow.keras import backend

backend.clear_session()

import nltk
nltk.download('stopwords')

from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords

import string

from keras.preprocessing.text import text_to_word_sequence
from keras.preprocessing.text import Tokenizer

import tensorflow as tf


from keras import backend

import subprocess as sb

backend.clear_session()

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
    dir_path = create_dir_for_phrase(phrase.replace(" ","_"))

    file_name = os.path.join(dir_path,phrase.replace(" ","_"))

    CMD = 'search_tweets.py --max-results 500 --results-per-call 100 --filter-rule "'+phrase+'" --filename-prefix '+file_name+"_"+randomString()+' --print-stream --credential-file twitter_api_info.yaml'
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
    df = produce_csv(objects,dir_path,phrase)

    downloaded_csvs = glob.glob(dir_path+"/csvs/"+"*.csv")

    for csv in downloaded_csvs:
        print("Merging:\t",csv)
        new_df = pd.read_csv(csv)
        df = pd.concat([df, new_df])

    print("Combined analysis has {} records".format(len(df)))

    #df = df.drop(['Unnamed: 0'],axis=1)

    print(dir_path+"/testinggggg.csv")
    df.to_csv(dir_path+"/testinggggg.csv")
    #process_individual(files,dir_path,phrase)
    #process.process_gender(df)
    complete_analysis = process.do_complete_analysis(df,dir_path,phrase)
    file_paths =  complete_analysis['file_paths']


    df = df[:10]
    df = df[['screen_name','full_text','gender']]
    print("Returning:",df)
    df = df.transpose()

    return {'data':df.to_dict(),
            'file_paths':file_paths,
            'analysis_obj': complete_analysis['analysis'],
            'sent_geo_analysis_obj': complete_analysis['geo_sent_analysis'],
            'google_analysis':"hello"}




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
    #i = (i+1)%2
    #user_info['sentiment'] = i

    pairs = {}
    if "retweeted_status" in tweet:
        user_info['type'] = 'retweet'
        pairs = handle_tweets(tweet['retweeted_status'])
    elif tweet['in_reply_to_status_id'] != "null":
        user_info['type'] = 'reply'

    pairs[tweet['id_str']] =  user_info




    return pairs




def produce_csv(obj,parent_dir,phrase):
    data = {}

    for tweet in obj:
        # Handle retweets
        results = handle_tweets(tweet) # possible recursive tweets, returns pairs of updates

        for k,v in results.items():
            data[k] = v

    #print(data)

    df = pd.DataFrame.from_dict(data)
    df = df.transpose()

    tf.compat.v1.reset_default_graph()
    sent_classifier, tk_obj = initialize_sentiment_classifier()

    sentences = df[['full_text']]
    to_predict = preprocessing(sentences,'full_text')
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



    #print(df)
    df.to_csv(os.path.join(parent_dir,phrase+"_"+randomString(10)+'.csv'), index=False)
    return df

def remove_punctuation(data):
    for punctuation in string.punctuation:
        if punctuation != '@':
            data = data.replace(punctuation, '')
    return data

def remove_trailing(data):
    data = data.replace('@',' ')
    return data



def preprocessing(data,col):
    data[col] = data[col].replace(to_replace=r'<br />',value="",regex=True)
    data[col] = data[col].replace(to_replace=r'http://t\.co/[A-Za-z0-9]{8}',value=" ",regex=True)
    data[col] = data[col].replace(to_replace=r'https://t\.co/[A-Za-z0-9]{8}',value=" ",regex=True)
    data[col] = data[col].str.lower()
    data[col] = data[col].apply(remove_punctuation)
    data[col] = data[col].replace(to_replace = r'@[A-Za-z0-9]*',value = 'AT_TOKEN',regex=True)
    data[col] = data[col].apply(remove_trailing)
    print("Removing stop words...")
    stop = stopwords.words('english')
    lem = WordNetLemmatizer()

    data[col] = data[col].apply(lambda x: " ".join([lem.lemmatize(word,'v') for word in word_tokenize(x)]))

    return data[col]


def initialize_sentiment_classifier():
    input_dim=137252
    EMBEDDING_DIM=200
    max_seq_length=200

    model_5 = Sequential()
    model_5.add(Embedding(input_dim, EMBEDDING_DIM, input_length=max_seq_length))
    model_5.add(LSTM(200))
    model_5.add(Dropout(0.2))
    model_5.add(Dense(4))
    model_5.add(Dropout(0.2))
    model_5.add(Dense(2, activation='softmax',name='sentiment_classifier'))
    model_5.compile(loss=["binary_crossentropy"], optimizer='adam', metrics=['accuracy'])
    print("Summary",model_5.summary())

    # Load weights
    model_5.load_weights('modellstm.hdf5')

    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)

    return model_5, tokenizer



def process_individual(list_of_files,parent_dir,phrase):
    for file in list_of_files:
        data = {}

        obj = []

        with open(file,"r") as readFile:
            for line in readFile:
                obj.append(json.loads(line))

        for tweet in obj:
            # Handle retweets
            results = handle_tweets(tweet) # possible recursive tweets, returns pairs of updates

            for k,v in results.items():
                data[k] = v

        #print(data)

        df = pd.DataFrame.from_dict(data)
        df = df.transpose()

        sent_classifier, tk_obj = initialize_sentiment_classifier()

        sentences = df[['full_text']]
        to_predict = preprocessing(sentences,'full_text')
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



        #print(df)
        df.to_csv(os.path.join(parent_dir,phrase+randomString(10)+'.csv'), index=False)
