#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 21 14:57:14 2020

@author: lakshmimenont
"""
import tweepy
import json
import datetime
import pandas as pd
import numpy as np

from sklearn import linear_model
import statsmodels.formula.api as smf
import statsmodels.api as sm
import matplotlib.pyplot as plt
from statsmodels.graphics.factorplots import interaction_plot

import nltk
nltk.download('vader_lexicon')

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

def getAirlineTweetsInDataFrame(airlineHandleList,columnNames):
    #columnNames = ['TweetText','TweetLength','HasHashtag', 'HasURL','UserFollowersCount','Retweets','Likes','CreatedAt']
    
    dfAllAirlineTweetsRead = pd.DataFrame(columns=columnNames) 
    
    for airlineHandle in airlineHandleList:
        airlineName  =  airlineHandle.replace("@"," ").strip()
        #dfAirlineTweets = readTweets(tweetsInJsonPath)
        dfTweetsRead = readTweets(airlineName,columnNames)
        dfAllAirlineTweetsRead = dfAllAirlineTweetsRead.append(dfTweetsRead)
        #print(dfTweetsRead)
    print(dfAllAirlineTweetsRead)
    return dfAllAirlineTweetsRead

def nltk_sentiment(sentence):
    
    from nltk.sentiment.vader import SentimentIntensityAnalyzer
    
    nltk_sentiment = SentimentIntensityAnalyzer()
    score = nltk_sentiment.polarity_scores(sentence)
    return score

def getCovIdStatus(createdAt):
    #Code for year
    if(createdAt.find('2020')!=-1):
        covId = 1
        
    else:
        covId = 0
    
    return covId
    

def readTweets(airlineName,columnNames):  
    tweetsInJsonPath = "/Users/lakshmimenont/Desktop/Working Python/TwitterCompetitiveStrategyProject/data/AirlinesMay26/tweetsInJsonFormat"+ airlineName +".json"
    with open(tweetsInJsonPath,"r") as readFile:
        dataRead = readFile.read()
        new_dataRead = dataRead.replace('}{', '},{')
        tweetsReadList = json.loads(f'[{new_dataRead}]')
    
    #print(type(tweetsReadList))
    
    dfTweetsRead = pd.DataFrame(columns=columnNames) 
    for tweetRead in tweetsReadList:
        #print(type(tweetRead))
        #print(tweetRead.get('in_reply_to_status_id'))
        #print(tweetRead.get('full_text'))
        #print(tweetRead.get('entities'))
        text = tweetRead.get('full_text')
        tweetWordCount = len(text)
        textSentimentScore  = nltk_sentiment(text)
        #print(type(textSentimentScore))
        #print(textSentimentScore)
        textPosSentiment = textSentimentScore.get('pos')
        textNegSentiment = textSentimentScore.get('neg')
        textNeuSentiment = textSentimentScore.get('neu')
        textCompoundSentiment= textSentimentScore.get('compound')
        
        entities = tweetRead.get('entities')
        if(entities.get('hashtags') == []):
            #print("Has no Hashtag")
            hashtag = 0
        else:
            hashtag = 1
            
        if(entities.get('urls') == []):
            #print("Has no URLS")
            url = 0
        else:
            url = 1
            
        if(entities.get('media') == [] or entities.get('media') == None):
            #print("Has no Media")
            media = 0
        else:
            media = 1
        
        
        #print(type(tweetRead.get('entities')))
        #print(tweetRead.get('user'))
        user = tweetRead.get('user')
        #rint(user.get('followers_count'))
        followersCount = int(user.get('followers_count'))
        
        #print(type(tweetRead.get('user')))
        retweet = int(tweetRead.get('retweet_count'))
        likes = int(tweetRead.get('favorite_count'))
        
        
        
        
        createdAt = tweetRead.get('created_at')
        #print(type(createdAt))
        #print(createdAt)
        covIdStatus = getCovIdStatus(createdAt)
        
        #postCovid
        dfTweetsRead.loc[airlineName+str(len(dfTweetsRead))] = [text, tweetWordCount, textPosSentiment, textNegSentiment, textNeuSentiment, textCompoundSentiment, hashtag, url, media, followersCount, retweet, likes, createdAt,covIdStatus]
        
        #print("\n")
        #if(tweetRead.get('in_reply_to_status_id')=='null' or tweetRead.get('in_reply_to_status_id')==None):
        #    print(tweetRead)
    return dfTweetsRead

def plotInteractionPlot(modelA):
    
    betaPreCovidPosSentCoeffA = modelA.params["TweetPosSentiment"]
    print("PreCovidPosSent Coefficient is " + str(betaPreCovidPosSentCoeffA))
    betaPreCovidNegSentCoeffA = modelA.params["TweetNegSentiment"]
    print("PreCovidNegSent Coefficient is " + str(betaPreCovidNegSentCoeffA))
    betaPostCovidPosSentCoeffA = modelA.params["TweetPosSentiment"] + modelA.params["interactCovidPosSent"]
    print("PostCovidPosSent Coefficient is " + str(betaPostCovidPosSentCoeffA))
    betaPostCovidNegSentCoeffA = modelA.params["TweetNegSentiment"] + modelA.params["interactCovidNegSent"]
    print("PostCovidNegSent Coefficient is " + str(betaPostCovidNegSentCoeffA))
    
    
    time = pd.Series(np.repeat(['PreCovid', 'PostCovid', 'PreCovid', 'PostCovid'], 15), name='Time')
    sentiment = pd.Series(np.repeat(['Positive_Sentiment', 'Negative_Sentiment'], 30), name='Sentiment')
    #betaCoeff = np.log(np.random.randint(1, 30, size=60))
    betaCoeff = pd.Series([betaPreCovidPosSentCoeffA,betaPostCovidPosSentCoeffA,betaPreCovidNegSentCoeffA,betaPostCovidNegSentCoeffA], name='BetaCoeff')
    
    fig, ax = plt.subplots(figsize=(6, 6))
    #fig = interaction_plot(x=time, trace=sentiment, response=betaCoeff, colors=['blue', 'red'], markers=['D', '^'], ms=10, ax=ax)
    
def analyseRetweetsWithinAirlines(dfAirlineTweetList):
    
    #print(dfAirlineTweetList)   
    modelRetweets = smf.ols(formula ='Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount',data= dfAirlineTweetList).fit()
    modelRetweets_details = modelRetweets.summary()
    #print(modelRetweets_details)
    
    #formulaRetweets = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount'
    #formulaRetweets = 'Retweets ~ TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount'
    formulaRetweets = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount + interactCovidNegSent'
    glm_Nbinomial = smf.glm(formula=formulaRetweets, data=dfAirlineTweetList,family=sm.families.NegativeBinomial())
    res_Nbinom = glm_Nbinomial.fit()
    res_Nbinom_details = res_Nbinom.summary()
    #print(res_Nbinom_details)
    
    #formulaRetweetsLogFoll = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount'
    #formulaRetweetsLogFoll = 'Retweets ~ TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount'
    #formulaRetweetsLogFoll = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount + interactCovidNegSent'
    #formulaRetweetsLogFoll = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount + interactCovidNegSent + interactCovidPosSent'
    formulaRetweetsLogFoll = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + HasMedia + logUserFollowersCount + interactCovidNegSent + interactCovidPosSent'
    glm_NbinomialLogFoll = smf.glm(formula=formulaRetweetsLogFoll, data=dfAirlineTweetList,family=sm.families.NegativeBinomial())
    res_NbinomLogFoll = glm_NbinomialLogFoll.fit()
    res_NbinomLogFoll_details = res_NbinomLogFoll.summary()
    print(res_NbinomLogFoll_details)
    plotInteractionPlot(res_NbinomLogFoll)
    
   
    modelLikes = smf.ols(formula ='Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount',data= dfAirlineTweetList).fit()
    
    modelLikes_details = modelLikes.summary()
    #print(modelLikes_details)
    return(res_NbinomLogFoll)

def analyseLikesWithinAirlines(dfAirlineTweetList):
    #print(dfAirlineTweetList)   
    
    #formulaLikes = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount'
    #formulaLikes = 'Likes ~ TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount'
    formulaLikes = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount + interactCovidNegSent'
    glm_Nbinomial = smf.glm(formula=formulaLikes, data=dfAirlineTweetList,family=sm.families.NegativeBinomial())
    res_Nbinom = glm_Nbinomial.fit()
    res_Nbinom_details = res_Nbinom.summary()
    #print(res_Nbinom_details)
    
    #formulaLikesLogFoll = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount'
    #formulaLikesLogFoll = 'Likes ~ TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount'
    #formulaLikesLogFoll = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount + interactCovidNegSent'
    #formulaLikesLogFoll = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount + interactCovidNegSent + interactCovidPosSent'
    formulaLikesLogFoll = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + HasMedia + logUserFollowersCount + interactCovidNegSent + interactCovidPosSent'
    glm_NbinomialLogFoll = smf.glm(formula=formulaLikesLogFoll, data=dfAirlineTweetList,family=sm.families.NegativeBinomial())
    res_NbinomLogFoll = glm_NbinomialLogFoll.fit()
    res_NbinomLogFoll_details = res_NbinomLogFoll.summary()
    print(res_NbinomLogFoll_details)
    
   
    modelLikes = smf.ols(formula ='Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount',data= dfAirlineTweetList).fit()
    
    modelLikes_details = modelLikes.summary()
    #print(modelLikes_details)
    return(res_NbinomLogFoll)

def displayDescriptiveStats(dfToDisplay,columnNames):
    for column in columnNames:
        print(column)
        if(column!='HasHashtag' and column!='HasURL' and column!='HasMedia'):
            print("Count is " + str(dfToDisplay[column].count()))
            print("Mean is " + str(dfToDisplay[column].mean()))
            print("Standard Deviation is " + str(dfToDisplay[column].std()))
            print("Min is "+str(dfToDisplay[column].min()))
            print("Max is "+str(dfToDisplay[column].max()))
            print("\n")
        else:
            print("Count is"+ str(dfToDisplay[column].sum()))
            print("\n")
            
            
def makeDataframeModifications(dfAirlineTweetList):
    dfAirlineTweetList[['TweetLength','TweetPosSentiment','TweetNegSentiment','TweetNeuSentiment','TweetCompoundSentiment','HasHashtag', 'HasURL','HasMedia','UserFollowersCount','Retweets','Likes','CovidStatus']] = dfAirlineTweetList[['TweetLength','TweetPosSentiment','TweetNegSentiment','TweetNeuSentiment','TweetCompoundSentiment','HasHashtag', 'HasURL','HasMedia','UserFollowersCount','Retweets','Likes','CovidStatus']].apply(pd.to_numeric)
    dfAirlineTweetList['logUserFollowersCount'] = np.log(dfAirlineTweetList['UserFollowersCount'])
    dfAirlineTweetList['interactCovidNegSent'] = dfAirlineTweetList['TweetNegSentiment'] * dfAirlineTweetList['CovidStatus']
    dfAirlineTweetList['interactCovidPosSent'] = dfAirlineTweetList['TweetPosSentiment'] * dfAirlineTweetList['CovidStatus'] 
    return dfAirlineTweetList

def displayCorrelationMatrix(dfAirlineTweetList,columnsToDisplay):
    dfCorrMatrix = pd.DataFrame(dfAirlineTweetList,columns = columnsToDisplay)
    print(dfCorrMatrix.dtypes)
    corrMatrix = dfCorrMatrix.corr()
    with pd.option_context('display.max_rows', 11, 'display.max_columns', None): 
        display(corrMatrix)
    
def main():
    gotAirlineHandleList = airlineHandleList()
    columnNames = ['TweetText','TweetLength','TweetPosSentiment','TweetNegSentiment','TweetNeuSentiment','TweetCompoundSentiment','HasHashtag', 'HasURL','HasMedia','UserFollowersCount','Retweets','Likes','CreatedAt','CovidStatus']
    
    dfAirlineTweetList  = getAirlineTweetsInDataFrame(gotAirlineHandleList,columnNames)
    dfAirlineTweetList = makeDataframeModifications(dfAirlineTweetList)
    columnsToDisplay = ['TweetLength','TweetPosSentiment','TweetNegSentiment','HasHashtag', 'HasURL','HasMedia','logUserFollowersCount','interactCovidNegSent','interactCovidPosSent','Retweets','Likes']
    #print(dfAirlineTweetList.dtypes)
    
    #displayDescriptiveStats(dfAirlineTweetList,columnsToDisplay)
    #displayCorrelationMatrix(dfAirlineTweetList,columnsToDisplay)
    
    analyseRetweetsWithinAirlines(dfAirlineTweetList)
    #analyseLikesWithinAirlines(dfAirlineTweetList)
        

main()


