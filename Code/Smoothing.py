from __future__ import division
import numpy as np
import UtilsTweetSafa as utils
import sys
import math

def getlinearcoefficients(language, grams, maxNgrams):
    lambdas = [0]*(maxNgrams)

    totalCount = grams[0].N()

    for maxgram in grams[maxNgrams-1].items():
        count = []
        count.append(maxgram[1])
        maxCount = maxgram[1]
        # print maxgram[0] # ngram
        # print maxgram[1] # count

        for gram in reversed(xrange(0, maxNgrams-1)):
            # print grams[gram].items()
            compare = maxgram[0][0:gram+1]
            if compare in grams[gram]:
                count.append(grams[gram].get(compare))
        count.append(totalCount)

        cases = list()
        max = 0.0
        temp = 0
        contador = 0
        for c in reversed(xrange(0, len(count)-1)):
            contador = contador + 1
            try:
                case = (count[c]-1)/(count[c+1]-1)
                if case >= max:
                    max = case
                    temp = contador-1
            except ZeroDivisionError:
                case = 0.0
            cases.append(case)

        lambdas[temp] = lambdas[temp] + maxCount

    linearCoefficients = list()

    linearCoefficients.append(language)

    for l in lambdas:
        linearCoefficients.append(l/sum(lambdas))


    return linearCoefficients


def getProbability(grams, lic, text, maxNgrams):
    text = tuple(text)
    totalCount = grams[0].N()
    count = []
    for gram in reversed(xrange(0, maxNgrams)):
        compare = text[0:gram + 1]

        if compare in grams[gram]:
            count.append(grams[gram].get(compare))
        else:
            count.append(0)

    count.append(totalCount)
    contador = 0
    probabilities = [0]*(maxNgrams)

    for c in reversed(xrange(0, len(count)-1)):
        contador = contador + 1
        try:
            prob = (lic[contador] * count[c])/(count[c+1])
        except ZeroDivisionError:
            prob = 0.0
        probabilities[contador-1] = prob
    return sum(probabilities)+0.00000000000001

def languageProbability(text, maxNgram, corpusNgrams, linearCoefficients):
    prob = 1.0
    for i in range(0, len(text)-maxNgram):
        t = list()
        for g in xrange(0, maxNgram):
            t.append(text[i+g])
            grams = []
            for gram in xrange(1, maxNgram+1):
                grams.append(corpusNgrams.get(str(gram)).get(linearCoefficients[0]))
        probability = getProbability(grams, linearCoefficients, t, maxNgram)
        prob = prob * probability
    return prob, linearCoefficients[0]

def getPredictedLanguageForTweet(linearCoefficients, text, maxNgram, corpusNgrams):
    maxProbability = 0
    average = 0
    predicted = dict()
    # import time
    # t0 = time.time()

    for linearCoefficient in linearCoefficients:
        prob, language = languageProbability(text, maxNgram, corpusNgrams, linearCoefficient)
        predicted[language] = prob
        if prob >= maxProbability:
            maxLanguage = language
            maxProbability = prob
        # sys.stdout.write("Sequence probability in "+str(language)+": "+str(prob)+"\n")
    # print "time for 1 probability= "+str(time.time()-t0)

    average = np.mean(predicted.values())
    threshold = (maxProbability-average)/10
    # print 'threshold '+str(threshold)
    languageSumed = utils.chooseLanguagesLin(predicted, threshold)
    # languageSumed = maxLanguage
    return languageSumed, maxProbability

def getlinearcoefficientsForLanguageArray(arrayLanguages, maxNgram, corpusNgrams):
    linearCoefficients = list()
    for language in arrayLanguages:
        grams = []
        for gram in xrange(1, maxNgram+1):
            grams.append(corpusNgrams.get(str(gram)).get(language))
        linearCoefficients.append(getlinearcoefficients(language, grams, maxNgram))
    return linearCoefficients


