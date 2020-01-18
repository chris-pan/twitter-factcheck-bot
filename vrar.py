import tweepy
import os
import time
import random


import json
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

api_key = os.environ['GOOGLE_KEY']
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_TOKEN = os.environ['ACCESS_TOKEN']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

FILE = 'lastuser.txt'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

def main(userQuery):
    factCheckService = build("factchecktools", "v1alpha1", developerKey=api_key)
    request = factCheckService.claims().search(query=userQuery, reviewPublisherSiteFilter = None)
    response = request.execute()
    reply = getAllRatings(response)
    return reply

def getRating(claim):
    review = claim["claimReview"][0]
    rating = ""

    if "textualRating" in review:
        rating = review["textualRating"]
    return rating

def getAllRatings(res):
    i = 0
    if "claims" in res.keys() and len(res["claims"]) > 0:
        for claim in res['claims']:
            rating = getRating(claim)
            if 'false' in rating.lower():
                i += 1
        return i/len(res['claims'])
    return 0

def get():
    f = open(FILE, 'r')
    id = f.read().strip()
    if id:
        id = int(id)
    f.close()
    return id
def store(num):
    f = open(FILE, 'w')
    f.write(str(num))
    f.close()
def reply():
    last = get()
    if last:
        mentions = api.mentions_timeline(last, tweet_mode='extended')
    else:
        mentions = api.mentions_timeline(tweet_mode='extended')
    for mention in reversed(mentions):
        rating = main(mention.full_text[11:])
        api.update_status('@' + mention.user.screen_name + " " + str(rating*100) + "% trustworthy", mention.id)
        last = mention.id
    store(last)
"""
while True:
    time.sleep(300)
    reply()
"""
reply()
