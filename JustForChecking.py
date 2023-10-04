#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 16:55:03 2020

@author: lakshmimenont
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May 17 17:32:56 2020

@author: lakshmimenont
"""

import tweepy
import json
import datetime

def authenticate():
    consumer_key = 'WeFnehzgqqzucdamDe9yf3Kdq'
    consumer_secret = '1OawBkUxDN7oHfIdBOi77iU1JJ3iQcH4f86PyiFb9pMMZJTSTH'
    
    access_token = '43929961-GAXeegcAtzVjtsNayVA9f84NkzimmTQR65Pw1jNcO'
    access_token_secret = 'Fue1Nmw28ugvLhwpm39xSQIeH4EXmmNDemHTJRMXuwVIt'
    
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    
    api = tweepy.API(auth,wait_on_rate_limit=True)
    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    
    return api

def downloadUserData(api,userList,noOfDays):
    
    end_date = datetime.datetime.now() - datetime.timedelta(days=noOfDays)
    for user in userList:
        userName  =  user.replace("@"," ").strip()
        tweetsInJsonPath = "/Users/lakshmimenont/Desktop/Working Python/TwitterCompetitiveStrategyProject/data/Users/tweetsInJsonFormat"+ userName +".json"
        tweetJsons = []
        for tweet in tweepy.Cursor(api.user_timeline, id=user,tweet_mode='extended',exclude_replies=True,include_rts=False).items(): 
            #print(f"{tweet.user.name} said: {tweet.full_text}")
            print(f"{tweet._json}") 
            #json.dumps converts dictionary to json string
            if tweet.created_at < end_date:
               break
            data = json.dumps(tweet._json)    
            tweetJsons.append(data)
            print("\n")
        with open(tweetsInJsonPath,"w") as f:
            for tweet in tweetJsons:
                f.write(tweet)

    
def main():
    
    gotApi = authenticate()
    userList = []
    user = '@hackiechan'
    userList.append(user)
    noOfDays = 10
    downloadUserData(gotApi,userList,noOfDays)

main()