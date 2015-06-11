# -*- coding: utf-8 -*-
from __future__ import division
from random import shuffle
import ReadData as read
import PreprocessTweets as preprocess
import UtilsTweetSafa as utils
import Smoothing as linear
import numpy as np
import CrossValidation as cv

import sys
import time

maxNgram = 8

# 1-. Read dataset and create tweetList fullfilled of Tweet object*

dataset_train = "../Dataset/output_complete.txt"
dataset_test = "../Dataset/test_complete.txt"
LI_Coefficients = "../Dataset/LICoefficients_10gram_for-train_complete_clean.txt"

tweetList_train = read.read_tweets_dataset(dataset_train)
tweetList_test = read.read_tweets_dataset(dataset_test)


# 2-. Pre-process state
# Raw data -> tweetList
#   Clean data -> tweetListPreProcessed

tweetListPreProcessed_train = preprocess.main(tweetList_train)
tweetListPreProcessed_test = preprocess.main(tweetList_test)
# shuffle(tweetListPreProcessed)

# 3-. Algorithms

# 3.1-. Algorithms: Bayesian Networks
#   3.2.1-. Linear interpolation
#       Generate linear coefficients: input (n-grams and language)
#       Smooth data

# cv.crossValidationLinearInterpolation(tweetListPreProcessed_train, 3, maxNgram)
linearCoefficientsAll = list()

trainDist, arrayLanguages, languagesAll = utils.obtainNgrams(tweetListPreProcessed_train, maxNgram)
for gram in xrange(1, maxNgram+1):
    linearCoefficientsAll.append(linear.getlinearcoefficientsForLanguageArray(arrayLanguages, gram, trainDist))

print linearCoefficientsAll

# linearCoefficientsALL = read.readLinearCoefficients(LI_Coefficients)


count = 4 # Desde que gram empezar

for i in xrange(count, maxNgram):
    count = count + 1
    t0 = time.time()

    for tweet in tweetListPreProcessed_test:
        # t0 = time.time()
        predictedLanguage, probability = linear.getPredictedLanguageForTweet(linearCoefficientsAll[i], tweet.text, count,
                                                                             trainDist)
        utils.printResultTXT(predictedLanguage, tweet, count)
    # print "time = "+str(time.time()-t0)  # cv.nestedCrossValidation(tweetListPreProcessed,5,5,[0,0,0],arrayLanguagesFull)
# cv.crossValidation(tweetListPreProcessed, 3, maxNgram+1)

# 3.3-. Out-of-place Measure
