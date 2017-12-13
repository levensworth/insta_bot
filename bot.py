import instabot
from instabot.api import API
from instabot.bot.bot_get import get_userid_from_username
import random
from tqdm import tqdm
import schedule
import time
from file_helpers import get_size

class UserBot(object):
    '''a class wrapper for the instabot bot and api
        it will be modify for our own use'''



    def __init__(self ,timeline_comment_path=None, whitelist= None, all_comments=None,
                like_first=False,follow_followers=False, amount=0
                , stop_words=['shop', 'store', 'free']):

        self.bot = instabot.Bot(stop_words=[])
        self.bot.proxy = "free-nl.hide.me"
        self.bot.login()
        self.timeline_comment = timeline_comment_path
        self.all_comments = all_comments
        self.like_after_follow = like_first
        self.follow_followers=follow_followers
        self.amount= amount
        if self.timeline_comment is not None:
            self.timeline_comment_number = get_size(self.timeline_comment)

        if self.all_comments is  not None:
            self.all_comments_number = get_size(self.all_comments)
        if whitelist is not None:
            self.add_whiteList(whitelist)




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
            white_file = open("whitelist.txt" , "a")
        except Exception as e:
            white_file = open("whitelist.txt" , "w")
        finally:
            for user in rest_users:
                white_file.write(str(user)+"\n")

            white_file.close()
            return True

    def like_hashtag(self, hashtag):
        media = self.bot.get_hashtag_medias(hashtag= hashtag)
        try:
            self.bot.like_medias(media)
            return True
        except Exception as e:
            print( " couldn't like hashstag %s" %hashtag)
            return False
    def follow_hashtag(self, hashtag):
        hastag_users = self.bot.get_hashtag_users(hashtag=hashtag)
        try:
            if self.follow_followers:
                for user in hastag_users:
                    self.follow_user_followers(user= user)
            self.bot.follow_users(hastag_users)
            return True
        except Exception as e:
            print(" could follow %s" %hashtag)
            return False
    def follow_per_location(self,new_location, amount=0):

        self.bot.searchLocation(new_location)
        finded_location = self.bot.LastJson['items'][0]

        counter = 0
        max_id = ''
        print("entre")
        with tqdm(total=amount) as pbar:
            while counter < amount:
                if self.bot.getLocationFeed(finded_location['location']['pk'], maxid=max_id):
                    location_feed = self.bot.LastJson
                    for media in self.bot.filter_medias(location_feed["items"][:amount], quiet=True):
                        user = self.bot.get_media_owner(media)
                        if self.bot.follow(user):
                            print( "user is " + str(user))
                            if self.like_after_follow:
                                self.like_lasts_media(user = user)
                            if self.follow_followers:
                                self.follow_user_followers(user_id=user)
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
                                self.like_lasts_media(user = self.bot.get_media_owner(media))
                            counter += 1
                            pbar.update(1)
                    if location_feed.get('next_max_id'):
                        max_id = location_feed['next_max_id']
                    else:
                        return False
        return True


    def like_user_feed(self, amount):
        self.bot.like_timeline(amount=amount)

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
            print('an error ocurred while trying to read the time_line comments file')

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


    def like_lasts_media(self,user, amount = 1):
        media = self.bot.get_user_medias(user_id=user)
        for x in range(0, amount):
            self.bot.like(media[x])
        return True



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
            self.bot.follow_followers(user_id=self.bot.get_userid_from_username(username))
        else:
            self.bot.follow_followers(user_id=user_id)

    def save_user_stats(self):
        self.bot.save_user_stats(self.bot.username)



def job_1(): bot.freeze_following()

def job_2( ):
    hashtags = ["photography", "summer", "beer", "party"]
    for tag in hashtags:
        bot.like_hashtag(tag)
        bot.follow_type(follow_type="hashtag", hashtags = [tag], amount=30)

def job_3():
    locations=["recoleta", "palermo", "olivos", "beccar", " san isidro"]
    for location in locations:
        bot.follow_type(follow_type="location", amount= 20, locations=[location])
        bot.like_location_feed(new_location=location, amount=20)

def job_4():
    bot.save_user_stats()

def job_5():
    bot.unfollow_non_followers()

def job_6():
    bot.unfollow_all()

def job_7():
    bot.comment_timeline()

def job_8():
    bot.like_user_feed(amount=25)
def job_9():
    bot.comment_timeline()
def job_10():
    bot.follow_user_followers("tiendanube")

bot = UserBot(timeline_comment_path= 'comments.txt',
                all_comments="comments.txt",
                follow_followers= True,
                amount= 10,
                like_first= True)


schedule.every(1).hours.do(job_4)
schedule.every(1).hours.do(job_2)
schedule.every(30).minutes.do(job_3)
schedule.every(2).days.at("16:00").do(job_6)
schedule.every(1).days.at("23:00").do(job_5)
schedule.every(1).hours.do(job_8)










if __name__ == '__main__':
    job_5() #save current followers

    while True:
        schedule.run_pending()
        time.sleep(1)
