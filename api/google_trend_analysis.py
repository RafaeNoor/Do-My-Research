from flask import Blueprint, render_template, session,abort
google_trend_analysis_file = Blueprint('google_trend_analysis_file',__name__)

from pytrends.request import TrendReq

from google_search_term import google_search
from summarize import summarize


pytrends = TrendReq()

import pandas as pd
import json


# Get top 3 UNIQUE related terms from top and rising
TOP_N = 2
SUMMARY_LENGTH = 8

@google_trend_analysis_file.route('/testing/<string:phrase>')
def get_related_terms(phrase):
    pytrends.build_payload(kw_list=[phrase])
    df = pytrends.related_queries()
    #print(df)
    top, rising = clean_related_queries(df,phrase)

    trend_results = {}

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
    print(list_of_urls)

    #TODO: Add link vetting process

    url = list_of_urls[0]

    if related_term == "definition":
        summary = summarize(url,2)['summary']
    else:
        summary = summarize(url,SUMMARY_LENGTH)['summary']

    summary += ["["+str(url)+"]"]


    return {related_term.capitalize(): summary}





