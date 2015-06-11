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

maxNgram = 5

# 1-. Read dataset and create tweetList fullfilled of Tweet object*

dataset = "../Dataset/output_complete.txt"
test = "../Dataset/mezclado.txt"
LI_Coefficients = "../Dataset/LICoefficients_5gram_for-output_complete.txt"

tweetList = read.read_tweets_dataset(dataset)
tweetListtest = read.read_tweets_dataset(test)
# 2-. Pre-process state

tweetListPreProcessed = preprocess.main(tweetList)
tweetListPreProcessedtest= preprocess.main(tweetListtest)
shuffle(tweetListPreProcessed)
    # Raw data -> tweetList
    # Clean data -> tweetListPreProcessed

#utils.printTweets(tweetListPreProcessed)

# 3-. Algorithms
#
# 3.1-. OBTAIN N-GRAMS

corpusNgrams, arrayLanguages, arrayLanguagesFull = utils.obtainNgrams(tweetListPreProcessed, maxNgram+1)
arrayLanguagesFull = utils.orderVector(arrayLanguagesFull)

# Example:  print(corpusNgrams.get(str(3)).get('pt'))


# 3.2-. Algorithms: Bayesian Networks
#   3.2.1-. Linear interpolation
#       Generate linear coefficients: input (n-grams and language)
#       Smooth data


tweetEN = "Tomorrow is going to be a good day to go to the beach."
tweetPT = "Amanhã será um dia muito bom, como ir para a praia."
tweetCA = "Demà farà un dia molt bo, com per anar a la platja."
tweetEU = "Bihar egun oso ona egingo du, hondartzara joateko modukoa."
tweetGL = "Mañá será un día moi bo, como ir á praia."
tweetES = "Mañana hará un dia muy bueno, como para ir a la playa."

realEN = "'Where is the moment when we need it the most' @ Salvador de Bahía, Brasil http://instagram.com/p/lX9he2CrnF/ "
realPT = "Faltam 11 dias para fazer anos, hmm"
realCA = "Comença al Centre Fraternal la Jornada de Cooperaciò i defensa dels DDHH al Sàhara Occidental pic.twitter.com/lmOEAfww7K"
realEU = "@ErrealaAle @rnrjukebox hori ere pentsatu det, km mordoxka zegoen bukaera arte bakarrik juteko,... bestela oso erraz jun da,..."
realGL = "Pouco frío tiña eu logo no carnaval en Abadín"
realES = "#Lugo #a6 (amarillo) obras en #PedrafitaDoCebreiro carril izquierdo cerrado km431,3~430 decreciente #dgt #trafico http://tuitrafico.com/estado-del-trafico/galicia/lugo/pedrafita-do-cebreiro/199833/ …"
realUND = "Hhhhhhhhhhhhjjhhhhhhhhhhhh"
realOTHER = "Buongiorno ai nostri ascoltatori in Italia :)) pic.twitter.com/zfGpYc3oxo"

a = 'Primer sorteo del stream @Dimegioclub http://www.twitch.tv/miicrocs' #en+es

b = 'Hau ez dakit zer den estamos hablando en un idioma edo beste batean'

c = '"En Cada Lucha Aquel Que Va A Muerte Es El Que Gana" Goazen @PasaiaRegional!! #aupaekipo #aupapasaia pic.twitter.com/BQ1ikdE2Qt'


text = preprocess.preprocessText(tweetEU)

# linearCoefficients = linear.getlinearcoefficientsForLanguageArray(arrayLanguages, maxNgram, corpusNgrams)
linearCoefficientsALL = read.readLinearCoefficients(LI_Coefficients)

linearCoefficients = linearCoefficientsALL[maxNgram-1]
import time
t1 = time.time()
for tweet in tweetListPreProcessedtest:
    t0 = time.time()

    predictedLanguage, probability = linear.getPredictedLanguageForTweet(linearCoefficients, tweet.text, maxNgram, corpusNgrams)
    utils.printResultTXT(predictedLanguage, tweet, 5)

    print "time for tweet= "+str(time.time()-t0)
print "time total= "+str(time.time()-t1)

# sys.stdout.write("\n    Tweet:  "+str(text.encode("utf-8")))
# sys.stdout.write("\n    Tweet language:   "+str(predictedLanguage)+"\n    Probability of:  "+str(probability)+"\n")


# 3.3-. Algorithms: Ranking Methods

# cv.nestedCrossValidation(tweetListPreProcessed,5,5,[0,0,0],arrayLanguagesFull)
# cv.crossValidation(tweetListPreProcessed, 3, [0,0,0], arrayLanguagesFull, maxNgram+1)

# 3.4-. Out-of-place Measure
