import instabot
from instabot.api import API
from instabot.bot.bot_get import get_userid_from_username
import random
from tqdm import tqdm
import time
from file_helpers import *
from mailer import send_notification
from like import *

base_path = "./storage/"
minimum = 1

def freeze_following(bot):
    ''' make a Whitelist with all your current following accounts'''
    your_following = bot.get_user_following(bot.user_id)
    already_whitelisted = bot.read_list_from_file(base_path+"whitelist.txt")
    rest_users = list(set(your_following) - set(already_whitelisted))
    random.shuffle(rest_users)

    try:
        white_file = open(base_path+"whitelist.txt" , "a")
    except Exception as e:
        white_file = open(base_path+"whitelist.txt" , "w")
    finally:
        for user in rest_users:
            white_file.write(str(user)+"\n")

        white_file.close()
        final_list = your_following.append(already_whitelisted)
        bot.add_whitelist(base_path+"whitelist.txt")
        return True


def follow_hashtag(bot, hashtag, follow_followers):
    hashtag_users = bot.get_hashtag_users(hashtag)
    try:
        if follow_followers:
            for user in hashtag_users:
                if not follow_user_followers(bot,user_id=user):
                    write_blacklist(bot.get_username_from_userid(user),bot)
        bot.follow_users(hashtag_users)
        return True
    except Exception as e:
        write_exception(" could not follow %s" %hashtag)
        return False


def follow_hashtag_per_location(bot= None,new_location=None,hashtag=None, amount=0,
like_after_follow=False, follow_followers=False):

    bot.searchLocation(new_location)
    finded_location = bot.LastJson['items'][0]

    counter = 0
    max_id = ''
    with tqdm(total=amount) as pbar:
        while counter < amount:
            if bot.getLocationFeed(finded_location['location']['pk'], maxid=max_id):
                location_feed = bot.LastJson

                for media in bot.filter_medias(location_feed["items"][:amount], quiet=True):
                    if contains_hashtag(bot.get_media_info(media), hashtag):
                        user = bot.get_media_owner(media)
                        if bot.follow(user):
                            print( "user is " + str(user))
                            if like_after_follow:
                                like_last_media(bot, user = user)
                            if follow_followers:
                                follow_user_followers(bot, user_id=user)
                            counter += 1
                            pbar.update(1)
                        append_to_black_list(self.bot,"followed.txt")
                if location_feed.get('next_max_id'):
                    max_id = location_feed['next_max_id']
                else:
                    return False

    return True

def contains_hashtag(media, hashtag):
    hashtag = "#" + str(hashtag)
    try:
        if hashtag in media[0]["caption"]["text"]:
            return True
    except Exception:
        return False



def follow_per_location(bot, new_location, amount=0, follow_followers=False, like_after_follow = False):

    bot.searchLocation(new_location)
    finded_location = bot.LastJson['items'][0]

    counter = 0
    max_id = ''
    with tqdm(total=amount) as pbar:
        while counter < amount:
            if bot.getLocationFeed(finded_location['location']['pk'], maxid=max_id):
                location_feed = bot.LastJson
                for media in bot.filter_medias(location_feed["items"][:amount], quiet=True):
                    user = bot.get_media_owner(media)
                    if bot.follow(user):
                        print( "user is " + str(user))
                        if like_after_follow:
                            like_last_media(bot, user = user)
                        if follow_followers:
                            follow_user_followers(bot,user_id=user)
                        #dispose the user
                        write_blacklist(bot.get_username_from_userid(user),bot)



                        counter += 1
                        pbar.update(1)

                if location_feed.get('next_max_id'):
                    max_id = location_feed['next_max_id']
                else:
                    return False
    return True



def follow_user_followers(bot,username=None, user_id=None):
    before =  bot.get_user_following(bot.user_id)
    if user_id is None:
        bot.follow_followers(user_id=bot.get_userid_from_username(username))
    else:
        bot.follow_followers(user_id=user_id)

    after = bot.get_user_following(bot.user_id)
    if (before+minimum) <= after:
        return True
    else:
        return False


def follow_file(bot, follow_file):
    if follow_file is None:
        return True
    try:
        follow_list = read_followers(follow_file)
        if len(follow_list) < 1:
            send_notification("USERS from {}".format(str(bot.username)),"no more user to follow!")

        for user in follow_list:
            if not follow_user_followers(bot,username = user):
                delete_follower(user, follow_file)
                write_blacklist(user,bot)
    except Exception as e:
        print(e)
        write_exception(str(e) + " follow_file()")
        return False


def follow_hashtag_per_location_file(bot, hashtags_file, max_likes_amount, like_after_follow=False, follow_user_followers=None):
    if hashtags_file is None:
        return False
    try:
        hashtags = read_hashtags(hashtags_file)
        locations = read_locations(locations_file)
        if(len(hashtags) == 0):
            write_exception("no more hashtags , all were comsumed!")
            send_notification("HASHTAGS from {}".format(str(bot.username)),"no more hashtags , all were comsumed!")
        for tag in hashtags:
            found = False
            for location in locations:
                if follow_hashtag_per_location(bot,hashtag=tag,new_location=location,
                amount=max_likes_amount, like_after_follow=like_after_follow, follow_followers=follow_followers):
                    found = True

            if not found:
                delete_hashtag(tag)
        return True
    except Exception as e:
        write_exception(str(e) + "from follow_hashtag_per_location")
        return False


def follow_hashtag_file(bot, hashtags_file, follow_followers):
    try:
        hashtags = read_hashtags(hashtags_file)
        for tag in hashtags:
            if not follow_hashtag(bot,hashtag=tag, follow_followers=follow_followers):
                delete_hashtag(tag)
        return True
    except Exception as e:
        print(e)
        write_exception(str(e) + "from follow_hashtag_file")
        return False


def follow_per_location_file(bot, max_following_amount, locations_file, like_after_follow=False):
    try:
        locations = read_locations(locations_file)
        for location in locations:
            follow_per_location(bot,new_location=location, amount=max_following_amount, like_after_follow=like_after_follow)
    except Exception as e:
        write_exception(str(e)+ " from follow_per_location")
