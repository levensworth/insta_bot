import instabot
from instabot.api import API
from instabot.bot.bot_get import get_userid_from_username
import random
from tqdm import tqdm
import schedule
import time
from file_helpers import *
from mailer import send_notification


def generate_report_for_user(bot):
    """ we use the blacklist generated from all the account the bot have interacted
        with and compares with the ones are currently following you"""
    try:
        user_follers = bot.get_user_followers(user_id=bot.user_id)
        interacted_accounts = read_blacklist()
        report = open(user_report_file)
        follow_back = count_follow_backs(user_follers, interacted_accounts)
        #TODO:
        # how to get a file just by the type of document
        growth = read_growth()

    except Exception as e:
        write_exception(e)


def count_follow_backs(followers_list, followed_list):

    count = 0

    for user in followed_list:
        if user is in followers_list:
            count = count+1

    return count


def read_growth():
    """this method will read the amount of followers in the last 24 hs and
    generate a vector containiing the slope of growth as well as the actual
    amount the amount of followers gained in this period """
    pass
