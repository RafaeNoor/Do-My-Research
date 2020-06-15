import requests

import json
from time import sleep

import pandas as pd


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
    "relevance",
    "top",
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
            res = requests.get("http://www.reddit.com/search.json?q={}&sort={}&limit=5".format(phrase,sort))
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

        other_with_user_info = get_all_users_info(other)

        df = pd.DataFrame.from_records(other_with_user_info)
        #df.to_csv("res_other.csv")

        if obj_idx == 0:
            comb_df = df
        else:
            comb_df = pd.concat([comb_df,df])

    print(comb_df)

    return comb_df




def get_reddit_posts(phrase):
    reddit_data = []

    print("Fetching posts...")
    for sort in sorts:
        reddit_data += search_reddit(phrase,sort,CYCLES)
        print("Done with SORT=",sort)

    df = filter_fields(reddit_data,fields)

    df.to_csv("{}_reddit.csv".format(phrase))
    print("Done with fetching reddit posts")


#get_reddit_posts("racism")

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





