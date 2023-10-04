#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 20 19:12:56 2020

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
    

def ecommerceHandleList():
    
    ecommerceAmazonHandle  = "@amazon"
    ecommerceWalmartHandle  = "@Walmart"
    ecommerceAlibabaGroupHandle  = "@AlibabaGroup" #scrapably fully 
    ecommerceJDCorporateHandle  = "@JD_Corporate" #scrapably fully
    ecommerceEBayHandle  = "@eBay" #scrapably fully
    ecommerceFlipkartHandle  = "@Flipkart" #scrapably fully
    ecommerceRakutenHandle  = "@Rakuten" #scrapably fully
    ecommerceTargetHandle  = "@Target" #scrapable 2-3 days
    
    
    ecommerceHandleList = []
    #ecommerceHandleList.append(ecommerceAmazonHandle)
    #ecommerceHandleList.append(ecommerceWalmartHandle)
    ecommerceHandleList.append(ecommerceAlibabaGroupHandle)
    ecommerceHandleList.append(ecommerceJDCorporateHandle)
    ecommerceHandleList.append(ecommerceEBayHandle)
    ecommerceHandleList.append(ecommerceFlipkartHandle)
    ecommerceHandleList.append(ecommerceRakutenHandle)
    #ecommerceHandleList.append(ecommerceTargetHandle)
    
    return ecommerceHandleList


def readTweets():  
    with open(tweetsInJsonPath,"r") as readFile:
        dataRead = readFile.read()
        new_dataRead = data.replace('}{', '},{')
        tweetsReadList = json.loads(f'[{new_dataRead}]')
    
    print(type(tweetsReadList))
    for tweetRead in tweetsReadList:
        print(type(tweetRead))
        print(tweetRead)

def downloadEcommerceData(api,ecommerceHandleList,noOfDays):
    
    end_date = datetime.datetime.now() - datetime.timedelta(days=noOfDays)
    for ecommerceHandle in ecommerceHandleList:
        ecommerceName  =  ecommerceHandle.replace("@"," ").strip()
        tweetsInJsonPath = "/Users/lakshmimenont/Desktop/Working Python/TwitterCompetitiveStrategyProject/data/EcommerceMay26/tweetsInJsonFormat"+ ecommerceName +".json"
        tweetJsons = []
        for tweet in tweepy.Cursor(api.user_timeline, id=ecommerceHandle,tweet_mode='extended',exclude_replies=True,include_rts=False).items(): 
            #print(f"{tweet.user.name} said: {tweet.full_text}")
            #print(f"{tweet._json}") 
            #json.dumps converts dictionary to json string
            if tweet.created_at < end_date:
               break
            data = json.dumps(tweet._json)    
            tweetJsons.append(data)
            #print("\n")
        counter = 0
        with open(tweetsInJsonPath,"w") as f:
            for tweet in tweetJsons:
                counter = counter + 1
                f.write(tweet)
        print("No Of Tweets are:" + str(counter))
        print("\n")
    
def main():
    
    gotApi = authenticate()
    gotEcommerceHandleList = ecommerceHandleList()
    print(gotEcommerceHandleList)
    noOfDays = 365
    downloadEcommerceData(gotApi,gotEcommerceHandleList,noOfDays)

main()
    