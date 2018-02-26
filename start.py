import instabot
from instabot.api import API
from instabot.bot.bot_get import get_userid_from_username
import random
from tqdm import tqdm
import schedule
import time
from file_helpers import *
from mailer import send_notification

from like import *
from follow import *
from comment import *
from stats import *
from unfollow import *

base_path = "./storage/"
base_expection_path = "./alerts/"
blacklist_path = base_path + "blacklist.txt"
whitelist_path = base_path + "whitelist.txt"
hashtags_file = base_path+"hashtags.txt"
comments_file ="comments.txt"
follow_file_path = base_path+"follow.txt"
locations_file = base_path+"locations.txt"
config_file = base_path+"config.txt"
user_report_file = base_path+"user_stats.csv"

class UserBot(object):
    '''a class wrapper for the instabot bot and api
        it will be modify for our own use'''

        #proxy = "free-nl.hide.me"

    def __init__(self ,timeline_comment_path=None, whitelist= None, all_comments=None,
                like_first=False,follow_followers=False
                , stop_words=None,proxy=None,
                followers=None, blacklist=None, hashtags=None,
                locations=None, config=None):


        filters = read_dict_file(config)
        self.bot = instabot.Bot(whitelist=whitelist,blacklist=blacklist,
             max_followers_to_follow=int(filters["max_followers_to_follow"]),
                 min_followers_to_follow=int(filters["min_followers_to_follow"]),
                 max_following_to_follow=int(filters["max_following_to_follow"]),
                 min_following_to_follow=int(filters["min_followers_to_follow"]),
                 max_followers_to_following_ratio=int(filters["max_followers_to_following_ratio"]),
                 max_following_to_followers_ratio=int(filters["max_following_to_followers_ratio"]),
                 min_media_count_to_follow=int(filters["min_media_count_to_follow"]),)
        self.bot.login()

        #my internal variables


        self.like_after_follow = like_first
        self.follow_followers=follow_followers
        self.max_following_amount = filters["follow_amount"]
        self.max_likes_amount = filters["like_amount"]
        self.linking_interval = filters["like_time"]
        self.following_interval = filters["follow_time"]
        self.config = filters
        #paths
        self.hashtags_file = hashtags
        self.timeline_comment = timeline_comment_path
        self.all_comments = all_comments



        if self.timeline_comment is not None:
            self.timeline_comment_number = get_size(self.timeline_comment)

        if self.all_comments is  not None:
            self.all_comments_number = get_size(self.all_comments)
        if whitelist is not None:
            self.add_whiteList(whitelist)

    def get_config(self):
        return self.config

    def add_blackList(self,path):
        self.bot.add_blacklist(path)

    def add_whiteList(self, path):
        self.bot.add_whitelist(path)

    def freeze_following(self):
        return freeze_following(self.bot)

    def like_hashtag(self, hashtag):
        return like_hashtag(self.bot, hashtag)

    def follow_hashtag(self, hashtag):
        return follow_hashtag(self.bot, hashtag, self.follow_followers)


    def follow_hashtag_per_location(self,new_location,hashtag, amount=0):
        return follow_hashtag_per_location(self.bot, new_location, hashtag, amount, self.like_after_follow, self.follow_followers)



    def follow_per_location(self,new_location, amount=0):
        follow_per_location(self.bot, new_location, amount, self.follow_followers)


    def like_location_feed(self, new_location, amount=0):
        return like_location_feed(bot, new_location, amount, self.like_after_follow)


    def like_user_feed(self, amount= 10):
        return like_user_feed(self.bot, amount)

    def unfollow_all(self):
        unfollow_all(self.bot)

    def unfollow_non_followers(self):
        unfollow_non_followers(self.bot)

    def unfollow_interacted_users(self):
        unfollow_interacted_users(self.bot, blacklist_path)

    def get_random_timeline_comment(self, path):
        try:
            comment_file = open(path, 'r')

            index = 1
            length = random.randrange(1,self.timeline_comment_number)
            for comment in comment_file:
                if index == length:
                    return str(comment)
                index = index + 1
        except Exception as e:
            write_exception('an error ocurred while trying to read the time_line comments file')

    def get_random_all_comment(self, path):
        try:
            comment_file = open(path, 'r')
            index = 1
            length = random.randrange(1,self.all_comment_number)
            for comment in comment_file:
                if index == length:
                    return str(comment)
                index = index + 1
        except Exception as e:
            print('an error ocurred while trying to read the comments file')

    def comment_timeline(self ):
        comment_timeline(self.bot, self.comment_timeline, self.timeline_comment_number)


    def like_last_media(self,user, amount = 1):
        return like_last_media(self.bot, user, amount)

    def follow_user_followers(self,username=None, user_id=None):
        follow_user_followers(self.bot, username, user_id)

    #FUNCTIONS BASED ON FILE OPERATIONS

    def follow_file(self):
        follow_file(self.bot, follow_file_path)

    def like_file_hashtags(self):
        return like_file_hashtags(self.bot, hashtags_file)

    def follow_hashtag_per_location_file(self):
        follow_hashtag_per_location_file(self.bot,self.hashtags_file, self.max_likes_amount,
         self.like_after_follow, self.follow_followers )

    def follow_hashtag_file(self):
        follow_hashtag_file(self.bot, self.hashtags_file,follow_followers=self.follow_followers)


    def like_location_feed_file(self):
        return like_location_feed_file(self.bot, self.max_likes_amount, locations_file)

    def follow_per_location_file(self):
        follow_per_location_file(self.bot, self.max_following_amount, locations_file, self.like_after_follow)

#FUNCTIONS BASED ON STATS

    def save_user_stats(self):
        self.bot.save_user_stats(self.bot.username)
        save_user_growth(self.bot)

    def generate_report_for_user(self):
        generate_report_for_user(self.bot)


#jobs for automation

def job_1():
    bot.freeze_following()

def job_2( ):
    bot.follow_hashtag_per_location_file()

def job_3():
    bot.like_location_feed_file()

def job_4():
    bot.save_user_stats()

def job_5():
    bot.unfollow_non_followers()

def job_6():
    bot.unfollow_interacted_users()

def job_7():
    bot.follow_per_location_file()

def job_8():
    bot.like_user_feed(amount=9)
def job_9():
    bot.follow_file()

def job_sleep():
    time.sleep(2000)



bot = UserBot(timeline_comment_path= base_path+'comments.txt',
                all_comments=base_path+"comments.txt",
                follow_followers= True,
                like_first= True,
                followers=base_path+"follow.txt",
                blacklist=base_path+"blacklist.txt",
                hashtags=base_path+"hashtags.txt",
                config =base_path+"config.txt",
                locations=base_path+"locations.txt",
                whitelist=base_path+"whitelist.txt"
                )




schedule.every(1).hours.do(job_4)
schedule.every(30).minutes.do(job_2)
schedule.every(45).minutes.do(job_9)
schedule.every(1).days.at("16:00").do(job_6)
schedule.every(1).days.at("23:00").do(job_5)
schedule.every(1).hours.do(job_8)
schedule.every(23).hours.do(job_sleep)
schedule.every(30).minutes.do(job_7)



if __name__ == '__main__':
    #setup(bot)
    job_4()
    while True:
        schedule.run_pending()
        time.sleep(1)
