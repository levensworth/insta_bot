import instabot
from instabot.api import API
from instabot.bot.bot_get import get_userid_from_username
import random
from tqdm import tqdm
import schedule
import time
from file_helpers import *
from mailer import send_notification

growth_file = "storage/growth.txt"

def generate_report_for_user(bot):
    """ we use the blacklist generated from all the account the bot have interacted
        with and compares with the ones are currently following you"""
    try:
        user_followers = bot.get_user_followers(user_id=bot.user_id)
        interacted_accounts = get_all_bot_users()
        report = open(user_report_file)
        follow_back = count_follow_backs(user_followers, interacted_accounts)
        average_likes = average_likes_per_n_post()

        #TODO:
        # how to get a file just by the type of document
        growth = read_growth()

    except Exception as e:
        write_exception(e)


def count_follow_backs(followers_list, followed_list):

    count = 0

    for user in followed_list:
        if user in followers_list:
            count = count+1

    return count


def average_likes_per_n_post(bot, number_of_posts= 10):
    likes = 0
    total = number_of_posts
    for post in bot.get_your_medias():
            if number_of_posts is 0:
                return likes
            else:
                number_of_posts -= 1

            likes += len(bot.get_media_likers())
    try:
        return likes / total
    except Exception:
        return 1


def save_user_growth(bot):
    """ the first column is the followers and the second is the following """

    followers =  len(bot.get_user_followers(bot.user_id))
    following = len(bot.get_user_following(bot.user_id))
    entry =  "{}    {}".format(str(followers), str(following))
    write_file(file_path= growth_file, array= [entry])


def read_growth():
    """this method will read the amount of followers in the last 24 hs and
    generate a vector containning the slope of growth as well as the actual
    amount the amount of followers gained in this period """

    
