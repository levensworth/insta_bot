import instabot
from instabot.api import API
from instabot.bot.bot_get import get_userid_from_username
import random
from tqdm import tqdm
import schedule
import time
from file_helpers import *
from mailer import send_notification


def like_hashtag(bot,hashtag):
    media = bot.get_hashtag_medias(hashtag= hashtag)
    try:
        return bot.like_medias(media)
    except Exception as e:
        write_exception( " couldn't like hashstag %s" %hashtag)
        return False

def like_location_feed(bot, new_location, amount=0, like_after_follow=False):

    bot.searchLocation(new_location)
    finded_location = bot.LastJson['items'][0]

    counter = 0
    max_id = ''
    with tqdm(total=amount) as pbar:
        while counter < amount:
            if bot.getLocationFeed(finded_location['location']['pk'], maxid=max_id):
                location_feed = bot.LastJson
                for media in bot.filter_medias(location_feed["items"][:amount], quiet=True):
                    if bot.like(media):
                        if like_after_follow:
                            like_last_media(user = bot.get_media_owner(media))
                        counter += 1
                        pbar.update(1)
                if location_feed.get('next_max_id'):
                    max_id = location_feed['next_max_id']
                else:
                    return False
    return True



def like_user_feed(bot, amount= 10):
    try:
        bot.like_timeline(amount=amount)
        return True
    except Exception as e:
        return False

def like_last_media(bot,user, amount = 1):
    try:
        media = bot.get_user_medias(user_id=user)
        for x in range(0, amount):
            bot.like(media[x])
        return True
    except Exception as e:
        return False


def like_file_hashtags(bot, hashtags_file=None, ):
    if hashtags_file is None:
        return False
    try:
        hashtags = read_hashtags(hashtags_file)
        if(len(hashtags) == 0):
            write_exception("no more hashtags , all were comsumed!")
            send_notification("HASHTAGS {}".format(str(bot.username)),"no more hashtags , all were comsumed!")
        for tag in hashtags:
            if not like_hashtag(bot, hashtag=tag):
                delete_hashtag(tag)
        return True
    except Exception as e:
        write_exception(str(e) + "from like_file_hashtags")
        return False

def like_last_media(bot,user, amount = 1):
    try:
        media = bot.get_user_medias(user_id=user)
        for x in range(0, amount):
            bot.like(media[x])
        return True
    except Exception as e:
        return False


def like_location_feed_file(bot, max_likes_amount, locations_file):
    try:
        locations = read_locations(locations_file)
        for location in locations:
            like_location_feed(bot,new_location=location, amount=max_likes_amount)
    except Exception as e:
        write_exception(e + " from like_location_feed_file")
