import pandas as pd
#import glob
import os
import matplotlib.pyplot as plt

import matplotlib

from matplotlib import use

import subprocess as sb

topN = 5

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

    file_paths.append(process_geography(males,"Males",parent_dir))
    file_paths.append(process_geography(females,"Females",parent_dir))

    file_paths.append(process_sentiment(males,"Males",parent_dir,topic))
    file_paths.append(process_sentiment(females,"Females",parent_dir,topic))

    return file_paths




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
    sizes_loc = df['location'].value_counts(normalize=True)
    print(sizes_loc[1:topN+1])

    fig_loc, ax_loc = plt.subplots()
    ax_loc.pie(sizes_loc[1:topN+1], labels=sizes_loc.index.to_list()[1:topN+1], autopct='%1.1f%%', shadow=True)
    ax_loc.axis('equal')
    plt.title("Location of the top {} most common locations for {}".format(topN,gender),y=-0.1)
    plt.show()
    plt.savefig(os.path.join(parent_dir,gender+"_geo.png"))

    return os.path.join(parent_dir,gender+"_geo.png")

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




