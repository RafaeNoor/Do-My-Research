import pandas as pd
#import glob
import os
import matplotlib.pyplot as plt

import matplotlib

from matplotlib import use

from google_trend_analysis import search_and_summarize_term

topN = 8

use('agg')

def process_gender(df):
    males = df[df['gender'].isin(['male','mostly_male','andy'])]
    females = df[df['gender'].isin(['female','mostly_female'])]

    #print("# Males:\t",len(males))
    #print("# Females:\t",len(females))

    return males,females


def do_complete_analysis(df,parent_dir,topic):
    locs = df.location.apply(normalize_locations)
    df['location'] = locs

    males, females = process_gender(df)


    file_paths = []
    gender_obj = {}

    fp, gender_obj['male'] = process_geography(males,"Males",parent_dir)
    file_paths.append(fp)
    fp, gender_obj['female'] = process_geography(females,"Females",parent_dir)
    file_paths.append(fp)

    analysis = analyze_geography(gender_obj,4,topic)
    #file_paths.append(process_geography(males,"Males",parent_dir))
    #file_paths.append(process_geography(females,"Females",parent_dir))

    file_paths.append(process_sentiment(males,"Males",parent_dir,topic))
    file_paths.append(process_sentiment(females,"Females",parent_dir,topic))

    sent_geo_res = sentiment_geo(df,parent_dir,topic)
    sent_geo_anal = sentiment_geo_analysis(sent_geo_res,4,topic)


    for key in sent_geo_res:
        file_paths.append(sent_geo_res[key]['path'])

    return {'file_paths' : file_paths, 'analysis': analysis, "geo_sent_analysis":sent_geo_anal}




def normalize_locations(loc):
    temp = pd.Series([loc])
    is_Null = temp.isnull().values.any()

    if is_Null:
        return "NULL"
    return_str = loc.lower()
    if "," in return_str:
        return_str = return_str.split(",")[-1].strip()
    if "/" in return_str:
        return_str = return_str.split("/")[-1].strip()
    return return_str


def process_geography(df,gender,parent_dir):
    plt.figure(dpi=350)
    df = df[df['location'] != 'NULL']
    sizes_loc = df['location'].value_counts(normalize=True)
    #print("SIZES LOC")
    #print(sizes_loc)
    #print(sizes_loc[1:topN+1])

    fig_loc, ax_loc = plt.subplots()
    ax_loc.pie(sizes_loc[:topN], labels=sizes_loc.index.to_list()[:topN], autopct='%1.1f%%', shadow=True)
    ax_loc.axis('equal')
    plt.title("Location of the top {} most common locations for {}".format(topN,gender),y=-0.1)
    #plt.show()
    plt.savefig(os.path.join(parent_dir,gender+"_geo.png"))

    return os.path.join(parent_dir,gender+"_geo.png") , sizes_loc.index.to_list()



# gender_obj = {male: [country1,2,3],...}
def analyze_geography(gender_obj, n,phrase):
    #print("hello")
    male = gender_obj['male'][:n]
    female = gender_obj['female'][:n]

    gender_union = len(list(set(male+female)))

    percentage_common = (2*n-gender_union) / n

    analysis_obj = {"desc":"","gendered":0}

    phrase = "'"+phrase.capitalize()+"'"

    if percentage_common >= 1.0:
        print("All countries in common")
        analysis_obj['desc'] = "Upon processing the data and analyzing how the top {} geography varies  " \
                               "with frequency of discussion on {} within Twitter users, there seems " \
                               "to be no indication that {} is a gendered issue. ".format(n,phrase,phrase)
        analysis_obj['gendered'] = 0

    elif percentage_common >= 0.70:
        analysis_obj['desc'] = "A majority of the top {} geographies are common across Male  " \
                               "and Female Twitter users when discussing {}. As most of the geographies overlap,  " \
                               "we are lead to believe that {} is not gendered".format(n,phrase, phrase)
        analysis_obj['gendered'] = 0
    elif percentage_common >= 0.5:
        analysis_obj['desc'] = "Approximately half of the top {} geographies are common across across Male  " \
                               "and Female Twitter users when discussing {}. Although there is some disparity  " \
                               "we are lead to believe that {} is not gendered" .format(n,phrase,phrase)
        analysis_obj['gendered'] = 0

    elif percentage_common >= 0.25:
        #print("Quarter countries in common")
        analysis_obj['desc'] = "There appears to be a stark difference amongst Twitter users top {} geographies  " \
                               "when discussing {}. This indicates a further naunced analysis is needed to characterize " \
                               "why this topic is gendered. While {} and {} dominate the discussion amongst females " \
                               ", males from {} and {} lead the discussion.".format(n,phrase,female[0],female[1],male[0],male[1])

        analysis_obj['gendered'] = 1

    else:

        analysis_obj['desc'] = "There appears to be virtually zero similarity mongst Twitter users geographies top {}" \
                               "when discussing {}. This neccessitates a further naunced analysis is needed to characterize " \
                               "why this topic is gendered. While {} and {} dominate the discussion amongst females " \
                               ", males from {} and {} lead the discussion.".format(n,phrase,female[0],female[1],male[0],male[1])

        analysis_obj['gendered'] = 1


    male_top = male[0]

    i = 0
    while female[i] == male_top:
        i+=1
    female_top = female[i]

    m1=search_and_summarize_term(phrase,male_top)
    f1=search_and_summarize_term(phrase,female_top)

    analysis_obj['google'] = {"location":[m1,f1]}

    return analysis_obj



def process_sentiment(df,gender,parent_dir,topic):
    plt.figure(dpi=350)
    labels = ['Negative', 'Positive']
    sizes = df['sentiment'].value_counts(normalize=True)
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True)
    ax.axis('equal')
    plt.title("Distribution of {} sentiment\n for {}".format(gender,topic))
    plt.show()
    plt.savefig(os.path.join(parent_dir,gender+"_"+topic+".png"))
    return os.path.join(parent_dir,gender+"_"+topic+".png")


def sentiment_geo(df,parent_dir,topic):
    pro = df[df['sentiment'] == 1]
    anti = df[df['sentiment'] == 0]

    plt.figure(dpi=350)
    pro = pro[pro['location'] != 'NULL']
    sizes_loc = pro['location'].value_counts(normalize=True)
    pro_list = sizes_loc.index.to_list()
    fig_loc, ax_loc = plt.subplots()
    ax_loc.pie(sizes_loc[:topN], labels=sizes_loc.index.to_list()[:topN], autopct='%1.1f%%', shadow=True)
    ax_loc.axis('equal')
    plt.title("Location of the top {} most common \nlocations for with {} sentiment on {}".format(topN,"Positive",topic),y=-0.1)
    #plt.show()
    plt.savefig(os.path.join(parent_dir,topic+"_"+"pro"+"_geo.png"))


    plt.figure(dpi=350)
    anti = anti[anti['location'] != 'NULL']
    sizes_loc_anti = anti['location'].value_counts(normalize=True)
    neg_list = sizes_loc_anti.index.to_list()
    fig_loc_anti, ax_loc_anti = plt.subplots()
    ax_loc_anti.pie(sizes_loc_anti[:topN], labels=sizes_loc_anti.index.to_list()[:topN], autopct='%1.1f%%', shadow=True)
    ax_loc_anti.axis('equal')
    plt.title("Location of the top {} most common \nlocations for with {} sentiment on {}".format(topN,"Negative",topic),y=-0.1)
    #plt.show()
    plt.savefig(os.path.join(parent_dir,topic+"_"+"neg"+"_geo.png"))




    return {"pro": {"path":os.path.join(parent_dir,topic+"_"+"pro"+"_geo.png"), "list":pro_list},
            "anti":{"path":os.path.join(parent_dir,topic+"_"+"neg"+"_geo.png"), "list":neg_list}}



def sentiment_geo_analysis(sent_obj,n,phrase):
    #print("hello")
    pro = sent_obj['pro']['list'][:n]
    anti = sent_obj['anti']['list'][:n]

    sent_union = len(list(set(pro+anti)))

    percentage_common = (2*n-sent_union) / n

    analysis_obj = {"desc":"","geo_varied":0}

    phrase = "'"+phrase.capitalize()+"'"

    if percentage_common >= 1.0:
        print("All countries in common")
        analysis_obj['desc'] = "Upon processing the data and analyzing how the top {} geography varies  " \
                               "with frequency of discussion and sentiment on {} within Twitter users, there seems " \
                               "to be no indication that {} is a geograhical biased issue. ".format(n,phrase,phrase)
        analysis_obj['geo_varied'] = 0

    elif percentage_common >= 0.70:
        analysis_obj['desc'] = "A majority of the top {} geographies are common across Pro-  " \
                               "and Anti- {} Twitter users when discussing {}. As most of the geographies overlap,  " \
                               "we are lead to believe that {} is not geographically biased".format(n,phrase,phrase, phrase)
        analysis_obj['geo_varied'] = 0
    elif percentage_common >= 0.5:
        analysis_obj['desc'] = "Approximately half of the top {} geographies are common across across Pro-  " \
                               "and Anti- {} Twitter users when discussing {}. Although there is some disparity  " \
                               "we are lead to believe that {} is not gendered" .format(phrase,n,phrase,phrase)
        analysis_obj['geo_varied'] = 0

    elif percentage_common >= 0.25:
        #print("Quarter countries in common")
        analysis_obj['desc'] = "There appears to be a stark difference geographically amongst Twitter users top {} geographies  " \
                               "when discussing {}. This indicates a further naunced analysis is needed to characterize " \
                               "why this topic is geographically biased. While {} and {} dominate the discussion amongst Pro-{} nations" \
                               ", Anti-{} from {} and {} lead the discussion.".format(n,phrase,pro[0],pro[1],phrase,phrase,anti[0],anti[1])

        analysis_obj['geo_varied'] = 1

    else:

        analysis_obj['desc'] = "There appears to be virtually zero similarity amongst Twitter users top {} geographies" \
                               "when discussing {}. This neccessitates a further naunced analysis to characterize " \
                               "why this topic is geographically. While {} and {} dominate the discussion amongst Pro-{} nations" \
                               ", Anti-{} from {} and {} lead the discussion.".format(n,phrase,pro[0],pro[1],phrase,phrase,anti[0],anti[1])

        analysis_obj['geo_varied'] = 1


    pro_top = pro[0]

    i = 0
    while anti[i] == pro_top:
        i+=1
    anti_top = anti[i]

    p1=search_and_summarize_term("pro "+phrase,pro_top)
    a1=search_and_summarize_term("anti "+phrase,anti_top)

    analysis_obj['twitter'] = {"sent_geo":[a1,p1]}

    return analysis_obj


