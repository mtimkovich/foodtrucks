#!/usr/bin/env python
import datetime as dt
import twitter
import yaml


def timestamp(time_str):
    return dt.datetime.strptime(time_str, '%a %b %d %H:%M:%S +0000 %Y')

with open('config.yml') as f:
    config = yaml.load(f)

# today = dt.today()
today = dt.date(2017, 8, 11)

acceptable_trucks = set('CurryUpNow')

api = twitter.Api(**config)
tweets = api.GetUserTimeline(screen_name='welovefoodeaze')
for tweet in tweets:
    # Get all tweets from today
    created_at = timestamp(tweet.created_at)

    if created_at.date() != today:
        break

    has_curry = any(m.screen_name in acceptable_trucks
            for m in tweet.user_mentions)

    print(has_curry)
    
    break
