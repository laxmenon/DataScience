#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 26 16:59:39 2020

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

import nltk
nltk.download('vader_lexicon')

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

def getEcommerceTweetsInDataFrame(ecommerceHandleList,columnNames):
    #columnNames = ['TweetText','TweetLength','HasHashtag', 'HasURL','UserFollowersCount','Retweets','Likes','CreatedAt']
    
    dfAllEcommerceTweetsRead = pd.DataFrame(columns=columnNames) 
    
    for ecommerceHandle in ecommerceHandleList:
        ecommerceName  =  ecommerceHandle.replace("@"," ").strip()
        #dfAirlineTweets = readTweets(tweetsInJsonPath)
        dfTweetsRead = readTweets(ecommerceName,columnNames)
        dfAllEcommerceTweetsRead = dfAllEcommerceTweetsRead.append(dfTweetsRead)
        #print(dfTweetsRead)
    print(dfAllEcommerceTweetsRead)
    return dfAllEcommerceTweetsRead

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

def readTweets(ecommerceName,columnNames):  
    tweetsInJsonPath = "/Users/lakshmimenont/Desktop/Working Python/TwitterCompetitiveStrategyProject/data/EcommerceMay26/tweetsInJsonFormat"+ ecommerceName +".json"
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
        #print(user.get('followers_count'))
        followersCount = int(user.get('followers_count'))
        
        #print(type(tweetRead.get('user')))
        retweet = int(tweetRead.get('retweet_count'))
        likes = int(tweetRead.get('favorite_count'))
        
        
        
        
        createdAt = tweetRead.get('created_at')
        #print(type(createdAt))
        covIdStatus = getCovIdStatus(createdAt)
        
        #postCovid
        dfTweetsRead.loc[ecommerceName+str(len(dfTweetsRead))] = [text, tweetWordCount, textPosSentiment, textNegSentiment, textNeuSentiment, textCompoundSentiment, hashtag, url, media, followersCount, retweet, likes, createdAt,covIdStatus]
        
        #print("\n")
        #if(tweetRead.get('in_reply_to_status_id')=='null' or tweetRead.get('in_reply_to_status_id')==None):
        #    print(tweetRead)
    return dfTweetsRead

def plotInteractionPlot(modelE):
    
    betaPreCovidPosSentCoeffE = modelE.params["TweetPosSentiment"]
    print("PreCovidPosSent Coefficient is " + str(betaPreCovidPosSentCoeffE))
    betaPreCovidNegSentCoeffE = modelE.params["TweetNegSentiment"]
    print("PreCovidNegSent Coefficient is " + str(betaPreCovidNegSentCoeffE))
    betaPostCovidPosSentCoeffE = modelE.params["TweetPosSentiment"] + modelE.params["interactCovidPosSent"]
    print("PostCovidPosSent Coefficient is " + str(betaPostCovidPosSentCoeffE))
    betaPostCovidNegSentCoeffE = modelE.params["TweetNegSentiment"] + modelE.params["interactCovidNegSent"]
    print("PostCovidNegSent Coefficient is " + str(betaPostCovidNegSentCoeffE))
    
    
    time = pd.Series(np.repeat(['PreCovid', 'PostCovid', 'PreCovid', 'PostCovid'], 15), name='Time')
    sentiment = pd.Series(np.repeat(['Positive_Sentiment', 'Negative_Sentiment'], 30), name='Sentiment')
    #betaCoeff = np.log(np.random.randint(1, 30, size=60))
    betaCoeff = pd.Series([betaPreCovidPosSentCoeffE,betaPostCovidPosSentCoeffE,betaPreCovidNegSentCoeffE,betaPostCovidNegSentCoeffE], name='BetaCoeff')
    
    fig, ax = plt.subplots(figsize=(6, 6))
    #fig = interaction_plot(x=time, trace=sentiment, response=betaCoeff, colors=['blue', 'red'], markers=['D', '^'], ms=10, ax=ax)
 
    

def analyseRetweetsWithinEcommerce(dfEcommerceTweetList):
    #print(dfEcommerceTweetList['interactCovidNegSent'])   
    modelRetweets = smf.ols(formula ='Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount',data= dfEcommerceTweetList).fit()
    modelRetweets_details = modelRetweets.summary()
    #print(modelRetweets_details)
    
    #formulaRetweets = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount'
    #formulaRetweets = 'Retweets ~ TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount'
    formulaRetweets = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount + interactCovidNegSent'
    glm_Nbinomial = smf.glm(formula=formulaRetweets, data=dfEcommerceTweetList,family=sm.families.NegativeBinomial())
    res_Nbinom = glm_Nbinomial.fit()
    res_Nbinom_details = res_Nbinom.summary()
    #print(res_Nbinom_details)
    
    #formulaRetweetsLogFoll = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount'
    #formulaRetweetsLogFoll = 'Retweets ~ TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount'
    #formulaRetweetsLogFoll = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount + interactCovidNegSent'
    #formulaRetweetsLogFoll = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount + interactCovidNegSent + interactCovidPosSent'
    formulaRetweetsLogFoll = 'Retweets ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + HasMedia + logUserFollowersCount + interactCovidNegSent + interactCovidPosSent'
    glm_NbinomialLogFoll = smf.glm(formula=formulaRetweetsLogFoll, data=dfEcommerceTweetList,family=sm.families.NegativeBinomial())
    res_NbinomLogFoll = glm_NbinomialLogFoll.fit()
    res_NbinomLogFoll_details = res_NbinomLogFoll.summary()
    print(res_NbinomLogFoll_details)
    plotInteractionPlot(res_NbinomLogFoll)
   
    modelLikes = smf.ols(formula ='Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount',data= dfEcommerceTweetList).fit()
    
    modelLikes_details = modelLikes.summary()
    #print(modelLikes_details)
    return(res_NbinomLogFoll)

def analyseLikesWithinEcommerce(dfEcommerceTweetList):
    #print(dfEcommerceTweetList['interactCovidNegSent'])   
    
    
    #formulaLikes = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount'
    #formulaLikes = 'Likes ~ TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount'
    formulaLikes = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount + interactCovidNegSent'
    glm_Nbinomial = smf.glm(formula=formulaLikes, data=dfEcommerceTweetList,family=sm.families.NegativeBinomial())
    res_Nbinom = glm_Nbinomial.fit()
    res_Nbinom_details = res_Nbinom.summary()
    #print(res_Nbinom_details)
    
    #formulaLikesLogFoll = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount'
    #formulaLikesLogFoll = 'Likes ~ TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount'
    #formulaLikesLogFoll = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount + interactCovidNegSent'
    #formulaLikesLogFoll = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + logUserFollowersCount + interactCovidNegSent + interactCovidPosSent'
    formulaLikesLogFoll = 'Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + HasMedia + logUserFollowersCount + interactCovidNegSent + interactCovidPosSent'
    glm_NbinomialLogFoll = smf.glm(formula=formulaLikesLogFoll, data=dfEcommerceTweetList,family=sm.families.NegativeBinomial())
    res_NbinomLogFoll = glm_NbinomialLogFoll.fit()
    res_NbinomLogFoll_details = res_NbinomLogFoll.summary()
    print(res_NbinomLogFoll_details)
    
   
    modelLikes = smf.ols(formula ='Likes ~ TweetLength + TweetPosSentiment + TweetNegSentiment + HasHashtag + HasURL + UserFollowersCount',data= dfEcommerceTweetList).fit()
    
    modelLikes_details = modelLikes.summary()
    #print(modelLikes_details)
    return(res_NbinomLogFoll)

def makeDataframeModifications(dfEcommerceTweetList):
    dfEcommerceTweetList[['TweetLength','TweetPosSentiment','TweetNegSentiment','TweetNeuSentiment','TweetCompoundSentiment','HasHashtag', 'HasURL', 'HasMedia','UserFollowersCount','Retweets','Likes','CovidStatus']] = dfEcommerceTweetList[['TweetLength','TweetPosSentiment','TweetNegSentiment','TweetNeuSentiment','TweetCompoundSentiment','HasHashtag', 'HasURL','HasMedia','UserFollowersCount','Retweets','Likes','CovidStatus']].apply(pd.to_numeric)
    dfEcommerceTweetList['logUserFollowersCount'] = np.log(dfEcommerceTweetList['UserFollowersCount'])
    dfEcommerceTweetList['interactCovidNegSent'] = dfEcommerceTweetList['TweetNegSentiment'] * dfEcommerceTweetList['CovidStatus']
    dfEcommerceTweetList['interactCovidPosSent'] = dfEcommerceTweetList['TweetPosSentiment'] * dfEcommerceTweetList['CovidStatus']
   
    return dfEcommerceTweetList
    
def displayDescriptiveStats(dfToDisplay,columnNames):
    for column in columnNames:
        print(column)
        if(column!='HasHashtag' and column!='HasURL'and column!='HasMedia'):
            print("Count is " + str(dfToDisplay[column].count()))
            print("Mean is " + str(dfToDisplay[column].mean()))
            print("Standard Deviation is " + str(dfToDisplay[column].std()))
            print("Min is "+str(dfToDisplay[column].min()))
            print("Max is "+str(dfToDisplay[column].max()))
            print("\n")
        else:
            print("Count is"+ str(dfToDisplay[column].sum()))
            print("\n")

def displayCorrelationMatrix(dfEcommerceTweetList,columnsToDisplay):
    dfCorrMatrix = pd.DataFrame(dfEcommerceTweetList,columns = columnsToDisplay)
    print(dfCorrMatrix.dtypes)
    corrMatrix = dfCorrMatrix.corr()
    with pd.option_context('display.max_rows', 11, 'display.max_columns', None): 
        display(corrMatrix)
        
def main():
    
    
    gotEcommerceHandleList = ecommerceHandleList()
    print(gotEcommerceHandleList)
    columnNames = ['TweetText','TweetLength','TweetPosSentiment','TweetNegSentiment','TweetNeuSentiment','TweetCompoundSentiment','HasHashtag', 'HasURL','HasMedia','UserFollowersCount','Retweets','Likes','CreatedAt','CovidStatus']
    
    dfEcommerceTweetList  = getEcommerceTweetsInDataFrame(gotEcommerceHandleList,columnNames)
    dfEcommerceTweetList = makeDataframeModifications(dfEcommerceTweetList)
    print(dfEcommerceTweetList.dtypes)
    columnsToDisplay = ['TweetLength','TweetPosSentiment','TweetNegSentiment','HasHashtag', 'HasURL','HasMedia','logUserFollowersCount','interactCovidNegSent','interactCovidPosSent','Retweets','Likes']
    
    #displayDescriptiveStats(dfEcommerceTweetList,columnsToDisplay)
    #displayCorrelationMatrix(dfEcommerceTweetList,columnsToDisplay)
    
    analyseRetweetsWithinEcommerce(dfEcommerceTweetList)  
    #analyseLikesWithinEcommerce(dfEcommerceTweetList) 


main()