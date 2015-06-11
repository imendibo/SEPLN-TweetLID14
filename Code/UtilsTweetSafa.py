from __future__ import division
import nltk as nk
import PreprocessTweets as preprocess

# This method concatenates tweets
def concatenateLanguageTweets(List):
    corpus = dict()
    languageArray = list()
    for tweet in List:
        if ~corpus.has_key(tweet.language) & (corpus.get(tweet.language) is None):
            corpus[tweet.language] = tweet.text
            languageArray.append(tweet.language)
        else:
            corpus[tweet.language] = corpus.get(tweet.language) + tweet.text
    return corpus, languageArray


# Separate by individual languages(en,es,eu,ca,gl,pt,und,other). Return a dictionary of individual languages
def separateIndividualLanguages(List):
    individualCorpus = dict()
    languageArray = list()
    for key in List.keys():
        if (not '+' in key) and (not '/' in key):
            individualCorpus[key] = List.get(key)
            languageArray.append(key)
            for subKey in List.keys():
                if key in subKey and not key is subKey:
                    individualCorpus[key] = individualCorpus[key] + List.get(subKey)
    return individualCorpus, languageArray


# N-gram Frequency distributions for all N and for all Languages.
# Returns Dictionary of maxNgrams dictionaries of each language.
# corpus.get(str(number)).get('language')

def freqDistributions(corpus, maxNgram):
    corpusNgrams = dict()
    for N in xrange(1, maxNgram):
        auxCorpus = dict()
        for key in corpus.keys():
            auxCorpus[key] = getFreqDist(corpus.get(key), N)
        corpusNgrams[str(N)] = auxCorpus
    return corpusNgrams


# returns N-gram distribution given a text
def getFreqDist(text, n):
    ngramsObject = nk.ngrams(text, n)
    freqDist = nk.FreqDist(ngramsObject)
    return freqDist


# Print tweets from an input list
def printTweets(tweetList):
    for tweet in tweetList:
        print tweet.text


# Obtain N-Grams from the tweet list
def obtainNgrams(tweetListPreProcessed, maxNgram):
    # Join all the tweets in one language. Return one dictionary of languages
    corpus, arrayLanguagesFull = concatenateLanguageTweets(tweetListPreProcessed)
    # individualLanguage=true:
    # Only individual languages(en,es,..)
    # individualLanguage=false:
    #       Mixed languages(en+es,pt+gl,..)
    individualLanguage = True
    if individualLanguage:
        corpus, arrayLanguages = separateIndividualLanguages(corpus)
    # clean dictionary of double spaces from concatenation
    for key in corpus.keys():
        corpus[key] = preprocess.remove_multiple_spaces(corpus.get(key))
    corpusNgrams = freqDistributions(corpus, maxNgram + 1)

    return corpusNgrams, arrayLanguages, arrayLanguagesFull


# Calculates out of place measure
def outofplaceMeasure(FDLenght, TTLenght, freqDist, freqDistTest, tweet):
    FDLenght = min(len(freqDist), FDLenght)
    TTLenght = min(len(freqDistTest), TTLenght)
    # Get m x n items
    topFDItems = freqDist.items()[:FDLenght]
    topTTItems = freqDistTest.items()[:TTLenght]
    totalDistance = 0
    for i in xrange(0, TTLenght):
        lp = topTTItems[i]
        distance = FDLenght
        for j in xrange(0, FDLenght):
            tp = topFDItems[j]
            if lp[0] == tp[0] or j == FDLenght - 1:
                distance = abs(i - j)
                totalDistance += distance
                break
    if FDLenght == 0:
        # print('Train')
        FDLenght = 1
    if TTLenght == 0:
        # print('Test'+'\t'+ tweet.language+'\t'+tweet.text)
        TTLenght = 1
    return totalDistance / (FDLenght * TTLenght)


# returns confidence of each N-gram to be a good guesser for a single tweet.

def learnNgramConfidences(confidenceDict, corpusNgrams, tweet, m, n):
    acc = 0
    tot = 0
    label = tweet.language
    for key in corpusNgrams.keys():
        predictedLanguage = list()
        languagesList = corpusNgrams.get(key).keys()
        for subkey in languagesList:
            predictedLanguage.append(
                outofplaceMeasure(m, n, corpusNgrams.get(key).get(subkey), getFreqDist(tweet.text, int(float(key))),
                                  tweet))
        predicted = languagesList[predictedLanguage.index(min(predictedLanguage))]
        if predicted in label:
            confidenceDict[key] = confidenceDict[key] + 1
            acc = acc + 1
        tot = tot + 1
    return confidenceDict, tot


# returns confidence of each N-gram to be a good guesser for a whole train set.
def learnNgramConfidencefromData(trainDist, trainSet):
    confidenceDict = dict((el, 0) for el in trainDist[0].keys())
    tot = 0
    for tweet in trainSet:
        confidenceDict, totAux = learnNgramConfidences(confidenceDict, trainDist[0], tweet, 80, 50)
        tot = tot + totAux
    confidenceDict = dict((el, confidenceDict.get(el) / tot) for el in confidenceDict.keys())
    return confidenceDict


# evaluate test Set
def evaluateNgramRakingSet(validationSet, trainFreq, confidenceNgrams, m, n):
    predictedLanguage = list()
    trueLanguage = list()
    for tweet in validationSet:
        trueLanguage.append(tweet.language)
        predictedLanguage.append(evaluateNgramRanking(tweet, trainFreq, confidenceNgrams, m, n))
    return predictedLanguage, trueLanguage


# evaluate single tweet
def evaluateNgramRanking(tweet, trainFreq, confidenceDict, m, n):
    acc = 0
    tot = 0
    if len(tweet.text) < 3:
        return 'und'
    label = tweet.language
    predictedDict = dict()
    for key in trainFreq[0].keys():
        predictedLanguage = list()
        languagesList = trainFreq[0].get(key).keys()
        for subkey in languagesList:
            predictedLanguage.append(
                outofplaceMeasure(m, n, trainFreq[0].get(key).get(subkey), getFreqDist(tweet.text, int(float(key))),
                                  tweet))
        predicted = languagesList[predictedLanguage.index(min(predictedLanguage))]
        if predicted in label:
            acc = acc + 1
        tot = tot + 1
        if not predictedDict.has_key(predicted):
            predictedDict[predicted] = confidenceDict.get(key)
        else:
            predictedDict[predicted] = predictedDict.get(predicted) + confidenceDict.get(key)
    predictedL = chooseLanguages(predictedDict, 0.05)
    return predictedL


# choose best languages
def chooseLanguages(predictedDict, threshold):
   items = [(v, k) for k, v in predictedDict.items()]
   items.sort()
   items.reverse()
   items = [(k, v) for v, k in items]
   language, value = items.pop(0)
   count = 0

   # if not language == 'other' and not language == 'und':
   for k, v in items:
       if count == 0:
           count += 1
           continue
       else:
           if value-v < threshold and count < 3:
               # if not k == 'other' and not k == 'und':
               language = language + '+' + k
               count += 1
   # else:
   #     if language == 'other':
   #         for k, v in items:
   #             if count == 0:
   #                 count += 1
   #                 continue
   #             else:
   #                 if value-v < threshold and count < 3 and not 'und':
   #                     if count == 1:
   #                         language = k
   #                     else:
   #                         language = language + '+' + k
   #                     count += 1
   #     elif language == 'und':
   #         for k, v in items:
   #                 if count == 0:
   #                     count += 1
   #                 else:
   #                     if value-v < threshold and count < 3 and not 'other':
   #                         if count == 1:
   #                             language = k
   #                         else:
   #                             language = language + '+' + k
   #                         count += 1
   # print('Decided Language: '+language)
   return language
def chooseLanguagesLin(predictedDict, threshold):
    items = [(prob, language) for language, prob in predictedDict.items()]
    items.sort()
    items.reverse()
    prob, language = items.pop(0)
    if not language == 'other' and not language == 'und':
        probNext, languageNext = items.pop(0)
        # print 'probnext '+str(probNext)+' threshold '+str(threshold)
        try:
            normProb = probNext / (probNext + threshold)
            normThres = threshold / (probNext + threshold)
        except:
            normProb = 0

        # print 'normprobnext '+str(normProb)+' normthreshold '+str(normThres)
        if normProb > 0.99:

        # if prob - threshold > probNext:
            if not languageNext == 'other' and not languageNext == 'und':
                language = language + '+' + languageNext
    return language


# order vector
def orderVector(arrayLanguagesFull):
    orderedVector = list()
    for el in arrayLanguagesFull:
        if (not '+' in el and not '/' in el and not 'other' in el and not 'und' in el):
            orderedVector.append(el)
    orderedVector.append('other')
    orderedVector.append('und')
    for el in arrayLanguagesFull:
        if ('+' in el):
            orderedVector.append(el)
    for el in arrayLanguagesFull:
        if ('/' in el):
            orderedVector.append(el)
    return orderedVector


# Print results file
def printResults(testSet, predictedList, ind):
    ind = ind + 1
    f = open('../Results/results.txt', 'a+')
    index = 0
    for tweet in testSet:
        f.write(tweet.id + '\t' + predictedList[index] + '\n')  # python will convert \n to os.linesep
        index += 1
    f.close()

def printResultTXT(predictedLanguage, tweet, count):
    file = open('../Results/resultLI-'+str(count)+'gramsDobleIdioma.txt', 'a+')
    file.write(tweet.id + '\t' + predictedLanguage + '\n')
    file.close()


# def printJeroni(true, predicted, ind):
#     ind = ind + 1
#     f = open('../DatasetJeroni/resultsJeroni%02d.txt' % ind, 'w')
#     for i in xrange(0, len(true)):
#         f.write('True:' + '\t' + true[i] + '\t' + 'Predicted;' + '\t' + predicted[
#             i] + '\n')  # python will convert \n to os.linesep
#     f.close()  # you c
