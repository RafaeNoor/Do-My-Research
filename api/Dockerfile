FROM python:3.7

RUN pip install Flask gunicorn sumy numpy pandas json google-api-python-client pytrends tensorflow keras matplotlib gender-guesser glob nltk

WORKDIR /

ENV PORT 8080

CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:api