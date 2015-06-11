from __future__ import division
import ReadData as read
import PreprocessTweets as preprocess
import UtilsTweetSafa as utils
import Smoothing as linear
import sys
import os

# __________________________________________________________________________
#
#
#
#                     Program to save in a file the
#             LINEAR INTERPOLATION COEFFICIENTS for a given dataset.
#
#     Use mode:
#             python CalculateLICoefficients.py <dataset> <N-grams>
#
#             e.g.
#                 python CalculateLICoefficients.py ../Dataset/output_complete.txt 5
#
#     This will generate a file with the linear coefficients from 1 to 5 grams.
#
#
#
# _____________________________________________________________________________


# 1-. Read dataset and create tweetList fullfilled of Tweet object*

dataset = sys.argv[1]
maxNgram = int(sys.argv[2])

filename = os.path.basename(dataset).split('.')

tweetList = read.read_tweets_dataset(dataset)

# 2-. Pre-process state
    # Raw data -> tweetList
    # Clean data -> tweetListPreProcessed
tweetListPreProcessed = preprocess.main(tweetList)

# 3-. OBTAIN N-GRAMS and Linear Coefficients

for i in xrange(5, maxNgram+1):
    corpusNgrams, arrayLanguages,arrayLanguagesFull = utils.obtainNgrams(tweetListPreProcessed, i+1)
    linearCoefficients = linear.getlinearcoefficientsForLanguageArray(arrayLanguages, i, corpusNgrams)
    # print linearCoefficients
    file = open('../Dataset/LICoefficients_'+str(maxNgram)+'gram_for-'+str(filename[0])+'.txt', 'a+')
    for li in linearCoefficients:
        file.write(str(i)+"\t"+str(li[0]))
        for co in xrange(1, i+1):
            file.write("\t"+str(li[co]))
        file.write("\n")
file.close()
