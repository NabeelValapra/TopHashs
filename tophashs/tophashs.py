import os, json, operator

from twython import Twython

TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY', '')
TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET', '')
OAUTH_TOKEN = os.environ.get('OAUTH_TOKEN', '')
OAUTH_TOKEN_SECRET = os.environ.get('OAUTH_TOKEN_SECRET', '')

twitter = Twython(TWITTER_CONSUMER_KEY,
                  TWITTER_CONSUMER_SECRET,
                  OAUTH_TOKEN,
                  OAUTH_TOKEN_SECRET)


def search_tweets(search_phrase, tweets_per_request=200, no_of_request=5):
    results = [twitter.search(q=search_phrase,
                              count=tweets_per_request,
                              result_type='recent')]

    if not results[-1]['statuses']:
        return []

    for _ in range(no_of_request-1):
        last_tweet_id = results[-1]['statuses'][-1]['id_str']

        results.append(
            twitter.search(
                q=search_phrase,
                count=tweets_per_request,
                max_id=last_tweet_id))

    tweets = []
    for result in results:
        for tweet in result['statuses']:
            tweets.append(tweet)

    return tweets


def get_top_hashtags(tweets, get_top=10):
    tops = {}
    for tweet in tweets:
        for hashtag in tweet['entities']['hashtags']:
            if hashtag['text'] not in tops.keys():
                tops[hashtag['text']] = 0
            tops[hashtag['text']] += 1

    if not tops:
        return None

    sorted_hashes = sorted(tops.items(), key=operator.itemgetter(1), reverse=True)

    top_hashtags = sorted_hashes[0:get_top]
    return json.dumps(top_hashtags.keys())
