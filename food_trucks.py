#!/usr/bin/env python
import datetime as dt
import os
from pushbullet import Pushbullet
import sys
import twitter
import yaml


def timestamp(time_str):
    return dt.datetime.strptime(time_str, '%a %b %d %H:%M:%S +0000 %Y')

os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open('config.yml') as f:
    config = yaml.load(f)

today = dt.datetime.today()

# Don't care on Mon or the weekend
if today.weekday() in set([0, 5, 6]):
    sys.exit()

acceptable_trucks = set(['CurryUpNow'])

pb = Pushbullet(config['pushbullet_token'])
api = twitter.Api(**config['twitter'])

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
