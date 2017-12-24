import instabot
from instabot.api import API
from instabot.bot.bot_get import get_userid_from_username
import random
from tqdm import tqdm
import schedule
import time
from file_helpers import *
from mailer import send_notification
<<<<<<< HEAD

from like import *
from follow import *
from comment import *
from stat import *
from unfollow import *
=======
>>>>>>> origin/master

base_path = "./storage/"
base_expection_path = "./alerts/"
hashtags_file = base_path+"hashtags.txt"
comments_file ="comments.txt"
<<<<<<< HEAD
follow_file_path = base_path+"follow.txt"
=======
follow_file = base_path+"follow.txt"
>>>>>>> origin/master
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
<<<<<<< HEAD
        return follow_hashtag(self.bot, hashtag, self.follow_followers)
=======
        hastag_users = self.bot.get_hashtag_users(hashtag=hashtag)
        try:
            if self.follow_followers:
                for user in hastag_users:
                    if not self.follow_user_followers(user_id=user):
                        write_blacklist(self.bot.get_username_from_userid(user))
            return self.bot.follow_users(hastag_users)
        except Exception as e:
            write_exception(" could not follow %s" %hashtag)
            return False
>>>>>>> origin/master


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
<<<<<<< HEAD
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
        follow_per_location_file(self.bot, self.max_following_amount, locations_file)
=======
        if self.follow_file is None:
            return True
        try:
<<<<<<< HEAD
            follow_list = read_followers(follow_file)

=======
            follow_list = read_followers(self.follow_file)
>>>>>>> origin/master
            if len(follow_file) <= 1:
                send_notification("USERS from {}".format(srt(self.bot.username)),"no more user to follow!")

            for user in follow_list:
                if not self.follow_user_followers(username = user):
                    delete_follower(user, follow_file)
                    write_blacklist(user)
        except Exception as e:
            print(e)
            write_exception(e)
            return False

    def like_file_hashtags(self):
        if self.hashtags_file is None:
            return False
        try:
            hashtags = read_hashtags(hashtags_file)
            if(len(hashtags) == 0):
                write_exception("no more hashtags , all were comsumed!")
                send_notification("HASHTAGS {}".format(str(self.bot.username)),"no more hashtags , all were comsumed!")
            for tag in hashtags:
                if not self.like_hashtag(hashtag=tag):
                    delete_hashtag(tag)
            return True

        except Exception as e:
            write_exception(str(e))
            return False

    def follow_hashtag_per_location_file(self):
        if self.hashtags_file is None:
            return False
        try:
            hashtags = read_hashtags(hashtags_file)
            locations = read_locations(locations_file)
            if(len(hashtags) == 0):
                write_exception("no more hashtags , all were comsumed!")
                send_notification("HASHTAGS from {}".format(str(self.bot.username)),"no more hashtags , all were comsumed!")
            for tag in hashtags:
                found = False
                for location in locations:
                    if self.follow_hashtag_per_location(hashtag=tag,new_location=location,amount=self.max_likes_amount):
                        found = True

                if not found:
                    delete_hashtag(tag)
            return True
        except Exception as e:
            write_exception(str(e))
            return False

    def follow_hashtag_file(self):
        try:
            hashtags = read_hashtags(hashtags_file)
            for tag in hashtags:
                if not self.follow_hashtag(hashtag=tag):
                    delete_hashtag(tag)
            return True
        except Exception as e:
            print(e)
            write_exception(e)
            return False
    def like_location_feed_file(self):
        try:
            locations = read_locations(locations_file)
            for location in locations:
                self.like_location_feed(new_location=location, amount=self.max_likes_amount)
        except Exception as e:
            write_exception(e)

    def follow_per_location_file(self):
        try:
            locations = read_locations(locations_file)
            for location in locations:
                self.follow_per_location(new_location=location, amount=self.max_following_amount)
        except Exception as e:
            write_exception(e)
>>>>>>> origin/master

#FUNCTIONS BASED ON STATS

    def save_user_stats(self):
        self.bot.save_user_stats(self.bot.username)

    def generate_report_for_user(self):
<<<<<<< HEAD
        generate_report_for_user(self.bot)
=======
        """ we use the blacklist generated from all the account the bot have interacted
            with and compares with the ones are currently following you"""
        try:
            user_follers = self.bot.get_user_followers(user_id=self.bot.user_id)
            interacted_accounts = read_blacklist()
<<<<<<< HEAD
            report = open(user_report_file)
=======
            report = open(base_path+"user stats")
>>>>>>> origin/master
        except Exception as e:
            write_exception(e)
>>>>>>> origin/master


def job_1():
    bot.freeze_following()

def job_2( ):
    bot.follow_hashtag_file()

def job_3():
    bot.like_location_feed_file()

def job_4():
    bot.save_user_stats()

def job_5():
    bot.unfollow_non_followers()

def job_6():
    bot.unfollow_all()

def job_7():
    bot.follow_per_location_file()

def job_8():
    bot.like_user_feed(amount=9)
def job_9():
    bot.follow_file()


bot = UserBot(timeline_comment_path= base_path+'comments.txt',
                all_comments=base_path+"comments.txt",
                follow_followers= True,
                like_first= True,
                followers=base_path+"follow.txt",
                blacklist=base_path+"blacklist.txt",
                hashtags=base_path+"hashtags.txt",
                config =base_path+"config.txt",
                locations=base_path+"locations.txt")



schedule.every(1).hours.do(job_4)
schedule.every(30).minutes.do(job_2)
schedule.every(45).minutes.do(job_9)
schedule.every(2).days.at("16:00").do(job_6)
schedule.every(1).days.at("23:00").do(job_5)
schedule.every(1).hours.do(job_8)
schedule.every(30).minutes.do(job_7)


if __name__ == '__main__':
<<<<<<< HEAD

=======
#    job_6()
#    job_1()
>>>>>>> origin/master
    job_9()
    while True:
        schedule.run_pending()
        time.sleep(1)
