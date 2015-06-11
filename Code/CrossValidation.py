from __future__ import division
import nltk as nk
import math
import Smoothing as linear
import UtilsTweetSafa as utils

def crossValidation(tweetList, k,maxNgram):
    m=80
    n=50
    for i in xrange(k):

        trainSet,testSet = divideDataset(tweetList,k,i)
        trainDist = utils.obtainNgrams(trainSet,maxNgram)
        confidenceDict=utils.learnNgramConfidencefromData(trainDist,trainSet)
        predicted, true=utils.evaluateNgramRakingSet(testSet,trainDist, confidenceDict,m,n)
        # utils.printJeroni(true,predicted,i)
        utils.printResults(testSet, predicted, i)


def divideDataset(dataset, k, index):
    if k == index-1:
        testSet = dataset[int(math.ceil(len(dataset)*index/k)):len(dataset)]
        trainSet = dataset[0:int(math.ceil(len(dataset)*index/k))]
    else:
        testSet = dataset[int(math.ceil(len(dataset)*index/k)):int(math.ceil(len(dataset)*(index+1)/k))]
        trainSet = dataset[0:int(math.ceil(len(dataset)*index/k))] + dataset[int(math.ceil(len(dataset)*(index+1)/k)):len(dataset)]
    return (trainSet,testSet)

def crossValidationLinearInterpolation(tweetList, k, maxNgram):
    for i in xrange(k):
        trainSet, testSet = divideDataset(tweetList, k, i)
        trainDist, arrayLanguages, languagesAll = utils.obtainNgrams(trainSet, maxNgram)
        linearCoefficients = linear.getlinearcoefficientsForLanguageArray(arrayLanguages, maxNgram, trainDist)
        print linearCoefficients
        count = 0
        tot = 0

        for tweet in testSet:
            predictedLanguage, probability = linear.getPredictedLanguageForTweet(linearCoefficients, tweet.text, maxNgram, trainDist)
            utils.printResultTXT(predictedLanguage, tweet)

            if(predictedLanguage == tweet.language):
                count = count + 1;
            tot = tot +1
            # print str(count)+'/'+str(tot)
        print 'correct tweets fold '+str(i)+' = '+str(count)+'/'+str(tot)
