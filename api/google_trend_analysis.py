from flask import Blueprint, render_template, session,abort
google_trend_analysis_file = Blueprint('google_trend_analysis_file',__name__)

from pytrends.request import TrendReq

from google_search_term import google_search, google_search_images
from summarize import summarize

from PyDictionary import PyDictionary
dictionary=PyDictionary()

pytrends = TrendReq()

import pandas as pd
import json


# Get top 3 UNIQUE related terms from top and rising
TOP_N = 3
SUMMARY_LENGTH = 8

@google_trend_analysis_file.route('/testing/<string:phrase>')
def get_related_terms(phrase):
    pytrends.build_payload(kw_list=[phrase])
    df = pytrends.related_queries()
    #print(df)
    top, rising = clean_related_queries(df,phrase)

    trend_results = {}

    print('top',top)
    print('rising',rising)

    trend_results['top'] = [search_and_summarize_term(phrase,term) for term in top[:TOP_N]]
    trend_results['rising'] = [search_and_summarize_term(phrase,term) for term in rising[:TOP_N]]

    return trend_results


def clean_related_queries(arg,phrase):
    top = arg[phrase]['top']
    top_stripped = top['query'].apply(lambda x: x.replace(phrase,'').strip()).unique()

    rising = arg[phrase]['rising']
    rising_stripped = rising['query'].apply(lambda x: x.replace(phrase,'').strip()).unique()


    return top_stripped,rising_stripped


def search_and_summarize_term(phrase,related_term):
    list_of_urls = google_search(phrase+" "+related_term)
    list_of_images = google_search_images(phrase+" "+related_term)
    print(list_of_urls)

    list_of_urls = [url for url in list_of_urls if "youtube" not in url]

    #TODO: Add link vetting process

    url_index = 0

    url = list_of_urls[url_index]
    img_url = list_of_images[url_index]


    while True:
        url = list_of_urls[url_index]
        citation_url = url
        try:
            print("[{}]Trying to Summarise:\t".format(related_term),url)
            if related_term == "definition":
                summary = get_english_def(phrase)#summarize(url,5)['summary']
                citation_url = "https://pypi.org/project/PyDictionary/"
                if summary == []: # if PyDict failed
                    summary = summarize(url,5)['summary']
                    citation_url = url
                else:
                    break

            else:
                summary = summarize(url,SUMMARY_LENGTH)['summary']

            if len(summary) >= SUMMARY_LENGTH:
                break
            else:
                url_index += 1
        except:
            print("Url {} failed .. Trying next url.".format(url))
            url_index+= 1


    #summary += [' <a href="'+str(url)+'">Citation</a> ',' <img src="'+str(img_url)+'"></img> ']

    #if related_term == "definition":
    #    citation_url = "https://pypi.org/project/PyDictionary/"


    return {related_term.capitalize():
        {
        "summary": summary,
        "citation": citation_url,
        "img": img_url,
        }
    }







def get_english_def(phrase):
    try:
        result = []
        meaning_obj = dictionary.meaning(phrase)

        for tk_type in meaning_obj:
            result.append(tk_type+":\t"+". ".join([sent.capitalize() for sent in meaning_obj[tk_type]]))

        syn_res =  dictionary.synonym(phrase)

        if syn_res == None:
            syn_res = ["none"]
        result = result + [" Synonyms:\t"] + syn_res
        return result
    except:
        return []