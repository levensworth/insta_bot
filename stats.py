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
    except Exception as e:
        write_exception(e)
