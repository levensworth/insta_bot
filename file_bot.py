import instabot
from instabot.api import API
from instabot.bot.bot_get import get_userid_from_username
import random
from tqdm import tqdm
import schedule
import time
from file_helpers import *

base_path = "./storage/"
base_expection_path = "./alerts/"
hashtags_file = "hashtags.txt"
comments_file ="comments.txt"



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
        ''' make a Whitelist with all your current following accounts'''
        your_following = self.bot.get_user_following(self.bot.user_id)
        already_whitelisted = self.bot.read_list_from_file("whitelist.txt")
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
            return True

    def like_hashtag(self, hashtag):
        media = self.bot.get_hashtag_medias(hashtag= hashtag)
        try:
            return self.bot.like_medias(media)
        except Exception as e:
            write_exception( " couldn't like hashstag %s" %hashtag)
            return False
    def follow_hashtag(self, hashtag):
        hastag_users = self.bot.get_hashtag_users(hashtag=hashtag)
        try:
            if self.follow_followers:
                for user in hastag_users:
                    if not self.follow_user_followers(user= user):
                        write_blacklist(self.bot.get_username_from_userid(user))
            return self.bot.follow_users(hastag_users)
        except Exception as e:
            write_exception(" could follow %s" %hashtag)
            return False


    def follow_hashtag_per_location(self,new_location,hashtag, amount=0):

        self.bot.searchLocation(new_location)
        finded_location = self.bot.LastJson['items'][0]

        counter = 0
        max_id = ''
        with tqdm(total=amount) as pbar:
            while counter < amount:
                if self.bot.getLocationFeed(finded_location['location']['pk'], maxid=max_id):
                    location_feed = self.bot.LastJson

                    for media in self.bot.filter_medias(location_feed["items"][:amount], quiet=True):
                        if self.contains_hashtag(self.bot.get_media_info(media), hashtag):
                            user = self.bot.get_media_owner(media)
                            if self.bot.follow(user):
                                print( "user is " + str(user))
                                if self.like_after_follow:
                                    self.like_last_media(user = user)
                                if self.follow_followers:
                                    self.follow_user_followers(user_id=user)
                                counter += 1
                                pbar.update(1)
                            append_to_black_list("followed.txt",self.bot)
                    if location_feed.get('next_max_id'):
                        max_id = location_feed['next_max_id']
                    else:
                        return False

        return True

    def contains_hashtag(self,media, hashtag):
        hashtag = "#" + str(hashtag)
        try:
            if hashtag in media[0]["caption"]["text"]:
                return True
        except Exception:
            return False



    def follow_per_location(self,new_location, amount=0):

        self.bot.searchLocation(new_location)
        finded_location = self.bot.LastJson['items'][0]

        counter = 0
        max_id = ''
        with tqdm(total=amount) as pbar:
            while counter < amount:
                if self.bot.getLocationFeed(finded_location['location']['pk'], maxid=max_id):
                    location_feed = self.bot.LastJson
                    for media in self.bot.filter_medias(location_feed["items"][:amount], quiet=True):
                        user = self.bot.get_media_owner(media)
                        if self.bot.follow(user):
                            print( "user is " + str(user))
                            if self.like_after_follow:
                                self.like_last_media(user = user)
                            if self.follow_followers:
                                if not self.follow_user_followers(user_id=user):
                                    write_blacklist(self.bot.get_username_from_userid(user))



                            counter += 1
                            pbar.update(1)

                    if location_feed.get('next_max_id'):
                        max_id = location_feed['next_max_id']
                    else:
                        return False
        return True


    def like_location_feed(self, new_location, amount=0):

        self.bot.searchLocation(new_location)
        finded_location = self.bot.LastJson['items'][0]

        counter = 0
        max_id = ''
        with tqdm(total=amount) as pbar:
            while counter < amount:
                if self.bot.getLocationFeed(finded_location['location']['pk'], maxid=max_id):
                    location_feed = self.bot.LastJson
                    for media in self.bot.filter_medias(location_feed["items"][:amount], quiet=True):
                        if self.bot.like(media):
                            if self.like_after_follow:
                                self.like_last_media(user = self.bot.get_media_owner(media))
                            counter += 1
                            pbar.update(1)
                    if location_feed.get('next_max_id'):
                        max_id = location_feed['next_max_id']
                    else:
                        return False
        return True


    def like_user_feed(self, amount= 10):
        try:
            self.bot.like_timeline(amount=amount)
            return True
        except Exception as e:
            return False

    def unfollow_all(self):
        self.bot.unfollow_everyone()

    def unfollow_non_followers(self):
        self.bot.unfollow_non_followers()


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
        medias = self.bot.get_timeline_medias()
        try:
            for media in medias:
                self.bot.comment(media_id=media, comment_text= self.get_random_timeline_comment(self.timeline_comment))
            return True

        except Exception as e:
            print(e)
            return False


    def like_last_media(self,user, amount = 1):
        try:
            media = self.bot.get_user_medias(user_id=user)
            for x in range(0, amount):
                self.bot.like(media[x])
            return True
        except Exception as e:
            return False


    def follow_type(self,follow_type =  'hashtag', amount = 1, user = None,
                    hashtags = [], locations = []):
        if follow_type is "hashtag":
            for tag in hashtags:
                self.follow_hashtag(tag)

        if follow_type is "location":
            for location in locations:
                self.follow_per_location(new_location = location, amount= amount)


    def follow_user_followers(self,username=None, user_id=None):
        if user_id is None:
            return self.bot.follow_followers(user_id=self.bot.get_userid_from_username(username))
        else:
            return self.bot.follow_followers(user_id=user_id)

    #FUNCTIONS BASED ON FILE OPERATIONS

    def follow_file(self):
        if self.follow_file is None:
            return True
        try:
            follow_list = read_followers(self.follow_file)
            for user in follow_list:
                if not self.follow_user_followers(username = user):
                    delete_follower(user, self.follow_file)
                    write_blacklist(user)
        except Exception as e:
            return False

    def like_file_hashtags(self):
        if self.hashtags_file is None:
            return False
        try:
            hashtags = read_hashtags(base_path+"hashtags.txt")
            if(len(hashtags) == 0):
                write_exception("no more hashtags , all were comsumed!")
            for tag in hashtags:
                if not self.like_hashtag(hashtag=tag):
                    delete_hashtag(tag)
            return True

        except Exception as e:
            wirte_exception(str(e))
            return False

    def follow_hashtag_per_location_file(self):
        if self.hashtags_file is None:
            return False
        try:
            hashtags = read_hashtags(base_path+"hashtags.txt")
            locations = read_locations(base_path+"locations.txt")
            if(len(hashtags) == 0):
                write_exception("no more hashtags , all were comsumed!")

            for tag in hashtags:
                found = False
                for location in locations:
                    if self.follow_hashtag_per_location(hashtag=tag,new_location=location,amount=self.max_likes_amount):
                        found = True

                if not found:
                    delete_hashtag(tag)
            return True
        except Exception as e:
            wirte_exception(str(e))
            return False

    def like_location_feed_file(self):
        try:
            locations = read_locations(base_path+"locations.txt")
            for location in locations:
                self.like_location_feed(new_location=location, amount=self.max_likes_amount)
        except Exception as e:
            write_exception(e)

    def follow_per_location_file(self):
        try:
            locations = read_locations(base_path+"locations.txt")
            for location in locations:
                self.follow_per_location(new_location=location, amount=self.max_following_amount)
        except Exception as e:
            write_exception(e)

    def save_user_stats(self):
        self.bot.save_user_stats(self.bot.username)




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
schedule.every(13).minutes.do(job_2)
schedule.every(9).minutes.do(job_9)
schedule.every(2).days.at("16:00").do(job_6)
schedule.every(1).days.at("23:00").do(job_5)
schedule.every(1).hours.do(job_8)


if __name__ == '__main__':
    job_1()
    while True:
        schedule.run_pending()
        time.sleep(1)
