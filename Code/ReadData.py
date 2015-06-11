import csv

# Create Tweet object to save all the necessary arguments of the tweets:
#   Arguments:
#       + id = username id
#       + name = username name
#       + languange = language of the tweet
#       + text = tweet text

class Tweet(object):
    id = 0
    name = ""
    language = ""
    text = ""

    # The class "constructor" - It's actually an initializer
    def __init__(self, id, name, language, text):
        self.id = id
        self.name = name
        self.language = language
        self.text = text

def make_tweet(id, name, language, text):
    tweet = Tweet(id, name, language, text)
    return tweet


# Read the tweet from the input dataset and get the values separated by the tab

def read_tweets_dataset(dataset):
    # Read TweetLID dataset
    tweetList = []
    with open(dataset) as file:
        for l in file.readlines():
            line = l.strip().split("\t")
            tweet = make_tweet(line[0], line[1], line[2], line[3])
            tweetList.append(tweet)
        file.close()
    return tweetList

def readLinearCoefficients(LIC_file):
    linearCoefficients = list()
    LIC = list()
    lan = list()
    tempLine = 1
    with open(LIC_file) as file:
        for line in csv.reader(file, dialect="excel-tab"):
            if not (line[0] == str(tempLine)):
                linearCoefficients.append(LIC)
                LIC = list()
                tempLine = tempLine + 1
            lan.append(line[1])
            for i in xrange(2, tempLine+2):
                lan.append(float(line[i]))
            LIC.append(lan)
            lan = list()

    linearCoefficients.append(LIC)
    return linearCoefficients