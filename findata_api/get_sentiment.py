import os
import requests
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
sentiment = SentimentIntensityAnalyzer()
from statistics import mean 


url = ('https://newsapi.org/v2/everything?'
       'q=Apple&'
       'from=2024-02-19&'
       'sortBy=popularity&'
       'apiKey=' + os.environ['NEWSAPI_KEY'])

response = requests.get(url)
articles = response.json()["articles"]

#print(response.json()["articles"][1]["content"])

neg, pos, neu, compound = [], [], [], []

for i in articles:
    score = sentiment.polarity_scores(i["content"])
    neg.append(score["neg"])
    pos.append(score["pos"])
    neu.append(score["neu"])
    compound.append(score["compound"])

print(mean(neg))
print(mean(pos))
print(mean(neu))
print(mean(compound))


