#!/usr/bin/env python3
import datetime as dt
from pushbullet import Pushbullet
import twitter
import yaml


def timestamp(time_str):
    return dt.datetime.strptime(time_str, '%a %b %d %H:%M:%S +0000 %Y')

with open('config.yml') as f:
    config = yaml.load(f)

acceptable_trucks = set(['CurryUpNow'])

pb = Pushbullet(config['pushbullet']['token'])
api = twitter.Api(**config['twitter'])

today = dt.datetime.today()
tweets = api.GetUserTimeline(screen_name='welovefoodeaze')
for tweet in tweets:
    # Get all tweets from today
    created_at = timestamp(tweet.created_at)

    if created_at.date() != today:
        break

    good_food = any(m.screen_name in acceptable_trucks
                    for m in tweet.user_mentions)

    if good_food:
        pb.push_note('Curry Up Now', 'is at the food trucks today!')
        break
