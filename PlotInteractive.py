#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  4 14:17:05 2020

@author: lakshmimenont
"""

def plotInteractionPlot(modelA,modelE):
    
    betaPreCovidPosSentCoeffA = modelA.params["TweetPosSentiment"]
    betaPreCovidNegSentCoeffA = modelA.params["TweetNegSentiment"]
    betaPostCovidPosSentCoeffA = modelA.params["TweetPosSentiment"] + modelA.params["interactCovidPosSent"]
    betaPostCovidNegSentCoeffA = modelA.params["TweetNegSentiment"] + modelA.params["interactCovidNegSent"]
    
    betaPreCovidPosSentCoeffE = modelE.params["TweetPosSentiment"]
    betaPreCovidNegSentCoeffE = modelE.params["TweetNegSentiment"]
    betaPostCovidPosSentCoeffE = modelE.params["TweetPosSentiment"] + modelE.params["interactCovidPosSent"]
    betaPostCovidNegSentCoeffE = modelE.params["TweetNegSentiment"] + modelE.params["interactCovidNegSent"]
    
    time = pd.Series(np.repeat(['PreCovid', 'PostCovid', 'PreCovid', 'PostCovid'], 15), name='Time')
    industry = pd.Series(np.repeat(['lo_carb', 'hi_carb'], 30), name='Industry')
    days = np.log(np.random.randint(1, 30, size=60))