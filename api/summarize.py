from __future__ import absolute_import
from __future__ import division, print_function, unicode_literals


from sumy.parsers.html import HtmlParser
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer as Summarizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words

LANGUAGE = "english"
SENTENCES_COUNT = 10


from flask import Blueprint, render_template, session,abort
summarize_file = Blueprint('summarize_file',__name__)

@summarize_file.route('/summary/<path:url>')
def summarize(url,sent_len = SENTENCES_COUNT):
    #url = "https://en.wikipedia.org/wiki/Automatic_summarization"
    parser = HtmlParser.from_url(url, Tokenizer(LANGUAGE))
    # or for plain text files
    # parser = PlaintextParser.from_file("document.txt", Tokenizer(LANGUAGE))
    stemmer = Stemmer(LANGUAGE)

    summarizer = Summarizer(stemmer)
    summarizer.stop_words = get_stop_words(LANGUAGE)


    return {'summary':[str(sentence) for sentence in summarizer(parser.document, sent_len)]}

