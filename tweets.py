import os
import tweepy as tw
import datetime as DT
import re
import demoji
import pandas as pd
consumer_key = "INSERT CONSUMER KEY HERE"
consumer_secret = "INSERT SECRET CONSUMER KEY HERE"
access_token = "INSERT ACCESS TOKEN HERE"
access_token_secret = "INSERT SECRET ACCESS TOKEN HERE"
auth = tw.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tw.API(auth, wait_on_rate_limit=True)


def getTweets(ticker, date):
    search_words = "$" + ticker + " AND ((I think) OR (bullish) OR (bearish) OR (bought) OR (sold) OR (buy) OR (sell) OR " \
                            "(dip) OR (gains) OR (sad) OR (happy) OR (feel) OR (makes me) OR (I'm) OR (I am))"
    search_words += " -filter:retweets" #ignore retweets to avoid skewed data
    tweets = tw.Cursor(api.search,
                       q=search_words,
                       lang="en",
                       tweet_mode='extended',
                       since=date).items()
    return tweets


# Call with a ticker and the # of days to analyze tweet data, numdays between 0 and 21
# Returns an array containing the tweets, if there is no tweets it is an empty array
def getTweetsWrapper(ticker, numDays):
    today = DT.date.today()
    date = today - DT.timedelta(days=numDays)
    return parseTweets(getTweets(ticker, date))


def parseTweets(tweets):
    newTweets = []
    for tweet in tweets:
        betterTweet = removeGarbage(tweet.full_text)
        if betterTweet is not None and len(betterTweet) is not 0:
            newTweets.append(betterTweet)
    return spamProtection(newTweets)
# Press the green button in the gutter to run the script.


def removeGarbage(tweet): # Removes links and non alphanumeric characters
    # We want to remove stuff the ML cant process, so @'s, links, maybe emojis?
    tweet = str(tweet)
    tweet = re.sub(r'http\S+', '', tweet) # Pretty easy to remove URLS, just an import
    tweet = re.sub(r'#', '', tweet)
    tweet = re.sub(r'@[A-Za-z0-9]+', '', tweet)

    tweet = tweet.replace("\n", " ")
    tweet = tweet.replace("\t", " ")
    tweet = tweet.replace("\r", " ")


    tweet = deEmojify(tweet)
    tweet = ' '.join(s for s in tweet.split(" ") if not shouldRemove(s))
    tweet = re.sub(' +', ' ', tweet)
    return tweet.strip()


def shouldRemove(word):
    string_check= re.compile('[@_!#$%^&*()<>?/\|}{~:]')
    if string_check.search(word) is None:
        return False
    else:
        return True


def deEmojify(text):
    return text.encode('ascii', 'ignore').decode('ascii')


# Removes repeat tweets, i.e. prevents spam. Only one spam will be counted.
def spamProtection(tweets):
    newTweets = []
    for tweet in tweets:
        if tweet not in newTweets:
            newTweets.append(tweet)

    return newTweets

# TEST THAT THIS CLASS WORKS
# if __name__ == '__main__':
#     ticker = "AAPL"
#     tweets = getTweetsWrapper(ticker, 0)
#     print(tweets)
#     print(len(tweets))
#     #parsedTweets = parseTweets(tweets)
#     #print(parsedTweets)
#     #print(len(parsedTweets))
#     # for twit in twits:
#     #     print(twit)
#         # body = twit.body
#         # print(body)
#     # print(test)

