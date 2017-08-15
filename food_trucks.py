#!/usr/bin/env python
import datetime as dt
import os
from pushbullet import Pushbullet
import sys
import twitter
import yaml


def timestamp(time_str):
    return dt.datetime.strptime(time_str, '%a %b %d %H:%M:%S +0000 %Y')


def join_english(lst):
    if len(lst) == 2:
        return '{0} and {1}'.format(*lst)
    else:
        return ', '.join(lst[:-2] + [', and '.join(lst[-2:])])


def make_msg(lst):
    lst = ['@' + i for i in lst]
    trucks = join_english(lst)
    verb = 'is' if len(lst) == 1 else 'are'

    return '{} {} at the food trucks today!'.format(trucks, verb)

os.chdir(os.path.dirname(os.path.realpath(__file__)))

with open('config.yml') as f:
    config = yaml.load(f)

today = dt.datetime.today()

# Only check Tue-Fri
if today.weekday() not in set(range(1, 5)):
    sys.exit()

acceptable_trucks = set(config['trucks'])

pb = Pushbullet(config['pushbullet_token'])
api = twitter.Api(**config['twitter'])

trucks_today = set()

tweets = api.GetUserTimeline(screen_name='welovefoodeaze')
for tweet in tweets:
    # Get all tweets from today
    created_at = timestamp(tweet.created_at)

    if created_at.date() != today.date():
        break

    for m in tweet.user_mentions:
        trucks_today.add(m.screen_name) 

good_food = list(trucks_today.intersection(acceptable_trucks))

if good_food:
    msg = make_msg(good_food)
    pb.push_note('Food Truck Alert!', msg)
