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
    

def airlineHandleList():
    
    airlineDeltaHandle  = "@Delta" #scrapable 0 or few days
    airlineAmericanAirlinesHandle  = "@AmericanAir" #scrapable  1-2 days
    airlineUnitedAirlinesHandle = "@united" #scrapable  1-2 days
    airlineSouthwestAirlinesHandle = "@SouthwestAir" #scrapable  1-2 days
    airlineChinaSouthernAirlinesHandle = "@CSAIRGlobal" #scrapable fully
    airlineAirCanadaHandle = "@AirCanada"
    airlineChinaEasternAirlinesHandle = "@CEAirglobal" #scrapable fully
    airlineLATAMAirlinesHandle = "@LATAMAirlines" #scrapable  1-2 days
    airlineAlaskaAirlinesHandle = "@AlaskaAir" #scrapable 4-5 days
    airlineJetBlueHandle = "@JetBlue"
    airlineSpiritAirlinesHandle = "@SpiritAirlines"
    airlineSkyWestAirlinesHandle = "@SkyWestAirlines" #scrapable fully but hardly any tweets
    airlineHawaiianAirHandle = "@HawaiianAir" #scrapable 0 or few days
    airlineAllegiantHandle = "@Allegiant"
    airlineMesaAirlinesHandle = "@MesaAirlines" #scrapable fully but hardly any tweets
    airlineAirindiainHandle = "@airindiain" #scrapable 0 or few days
    airlineLufthansaHandle = "@lufthansa" #Can scrape one day or few
    airlineAustrianAirlinesHandle = "@_austrian" #scrapable fully
    airlineScandinavianAirlinesHandle = "@SAS"
    
    
    airlineHandleList = []
    #airlineHandleList.append(airlineDeltaHandle)
    #airlineHandleList.append(airlineAmericanAirlinesHandle)
    #airlineHandleList.append(airlineUnitedAirlinesHandle)
    #airlineHandleList.append(airlineSouthwestAirlinesHandle)
    airlineHandleList.append(airlineChinaSouthernAirlinesHandle)
    #airlineHandleList.append(airlineAirCanadaHandle)
    airlineHandleList.append(airlineChinaEasternAirlinesHandle)
    #airlineHandleList.append(airlineLATAMAirlinesHandle)
    #airlineHandleList.append(airlineAlaskaAirlinesHandle)
    #airlineHandleList.append(airlineJetBlueHandle)
    #airlineHandleList.append(airlineSpiritAirlinesHandle)
    airlineHandleList.append(airlineSkyWestAirlinesHandle)
    #airlineHandleList.append(airlineHawaiianAirHandle)
    #airlineHandleList.append(airlineAllegiantHandle)
    airlineHandleList.append(airlineMesaAirlinesHandle)
    #airlineHandleList.append(airlineAirindiainHandle)
    #airlineHandleList.append(airlineLufthansaHandle)
    airlineHandleList.append(airlineAustrianAirlinesHandle)
    #airlineHandleList.append(airlineScandinavianAirlinesHandle)
    
    return airlineHandleList


def readTweets():  
    with open(tweetsInJsonPath,"r") as readFile:
        dataRead = readFile.read()
        new_dataRead = data.replace('}{', '},{')
        tweetsReadList = json.loads(f'[{new_dataRead}]')
    
    print(type(tweetsReadList))
    for tweetRead in tweetsReadList:
        print(type(tweetRead))
        print(tweetRead)

def downloadAirlineData(api,airlineHandleList,noOfDays):
    
    end_date = datetime.datetime.now() - datetime.timedelta(days=noOfDays)
    for airlineHandle in airlineHandleList:
        airlineName  =  airlineHandle.replace("@"," ").strip()
        tweetsInJsonPath = "/Users/lakshmimenont/Desktop/Working Python/TwitterCompetitiveStrategyProject/data/AirlinesMay26/tweetsInJsonFormat"+ airlineName +".json"
        tweetJsons = []
        print("Im here")
        for tweet in tweepy.Cursor(api.user_timeline, id=airlineHandle,tweet_mode='extended',exclude_replies=True,include_rts=False).items(): 
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
    gotAirlineHandleList = airlineHandleList()
    print(gotAirlineHandleList)
    noOfDays = 365
    downloadAirlineData(gotApi,gotAirlineHandleList,noOfDays)


main()
    
