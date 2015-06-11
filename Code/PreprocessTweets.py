import ReadData as read
import re
import string

punctuation = '!\"#$%&()*+,-./:;<=>?[\]^`{|}~'

def lower_case(tweet):
    return tweet.decode('utf-8').lower()

def remove_multiple_spaces(tweet):
    tweet = ' ' + tweet + ' '
    tweet = re.sub(' +',' ',tweet)
    return tweet

def remove_puntuation(tweet):
    return reduce(lambda tweet, c: tweet.replace(c, ' '), punctuation, tweet)

def format_puntuation(tweet):
    return reduce(lambda tweet, c: tweet.replace(c, ' ' + c + ' '), punctuation, tweet)

def remove_url(tweet):
    return re.sub(r'\w+:\/{2}[\d\w-]+(\.[\d\w-]+)*(?:(?:\/[^\s/]*))*', '', tweet)

def remove_usernames(tweet):
    return re.sub('@\s*\w+\s*', '', tweet)

def remove_pic_twitter(tweet):
    return re.sub('pic.twitter[^\s|,]+', '', tweet)

def remove_vowel_repetitions(tweet):
    # return re.sub(r'(.)\1\1+', r'\1\1', tweet) #dos
    return re.sub(r'(.)\1\1+', r'\1', tweet) #uno

def remove_numbers(tweet):
    return re.sub('[0-9]', '', tweet)

def remove_emoticons(tweet):
    return tweet

def preprocessText(tweet):
    tweetPreprocessed = lower_case(tweet)
    tweetPreprocessed = remove_pic_twitter(tweetPreprocessed)
    tweetPreprocessed = remove_url(tweetPreprocessed)
    tweetPreprocessed = format_puntuation(tweetPreprocessed)
    tweetPreprocessed = remove_usernames(tweetPreprocessed)
    tweetPreprocessed = remove_puntuation(tweetPreprocessed)
    tweetPreprocessed = remove_multiple_spaces(tweetPreprocessed)
    tweetPreprocessed = remove_vowel_repetitions(tweetPreprocessed)
    #tweetPreprocessed = remove_emoticons(tweetPreprocessed) #TODO
    tweetPreprocessed = remove_numbers(tweetPreprocessed)
    tweetPreprocessed = remove_emoticons(tweetPreprocessed)
    return tweetPreprocessed

def main(tweetList):
    tweetListPreprocessed = []
    tweetPreprocessed = ""

    for tweet in tweetList:
        if (tweet.text != 'Not Available'):
            tweetPreprocessed = preprocessText(tweet.text)

            # Save in new object
            tweetPre = read.make_tweet(tweet.id, tweet.name, tweet.language, tweetPreprocessed)
            tweetListPreprocessed.append(tweetPre)

    return tweetListPreprocessed
