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


def get_search_tweets(search_phrase, tweets_per_request=200, no_of_request=5):
    results = [twitter.search(q=search_phrase,
                              count=tweets_per_request,
                              result_type='popular')]

    for _ in range(no_of_request-1):
        last_tweet_id = results[-1]['statuses'][-1]['id_str']

        results.append(
            twitter.search(
                q=search_phrase,
                count=tweets_per_request,
                max_id=last_tweet_id))

    for result in results:
        for tweet in result['statuses']:
           yield tweet


def get_top_hashtags(search_phrase):
    tops = {}
    for tweet in get_search_tweets(search_phrase):
        for hashtag in tweet['entities']['hashtags']:
            if hashtag['text'] not in tops.keys():
                tops[hashtag['text']] = 0
            tops[hashtag['text']] += 1

    sorted_hashes = sorted(tops.items(), key=operator.itemgetter(1), reverse=True)
    return json.dumps(sorted_hashes)
