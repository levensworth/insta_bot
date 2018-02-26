import csv
import time
base_path = "./storage/"
base_expection_path = "./alerts/"
hashtags_file = "hashtags.txt"
"""
ALL FILES ONLY USE USERNAME NO ID WILL BE RECORDED AS A MATTER OF SIMPLICITY FOR
THE FINAL USER

"""

def get_size(path):
    with open(path,'r') as f:
        for i, l in enumerate(f):
            pass
    return i + 1


def read_dict_file(file_path):
    file_dict = csv.DictReader(open(file_path,"r"))
    file_dictionary = {}
    string_dictionary = file_dict.__next__()
    for item in string_dictionary:
        file_dictionary[item]= int(string_dictionary[item])
    return file_dictionary


def read_followers(file_path):
    file_array = open(file_path,"r")
    arr = []
    for line in file_array:
        arr.append(line.replace("\n",""))

    return arr

def read_hashtags(file_path):
    file_array = open(file_path,"r")
    arr = []
    for line in file_array:
        arr.append(line.replace("\n",""))

    return arr


def write_file(file_path,array, delimiter="\n"):
    try:
        new_file = open(file_path,'w')
        for x in array:
            new_file.write(str(x)+delimiter)
        return True
    except Exception as e:
        print(e)
        return False


def delete_follower(username, file_path):
    try:
        follow_array = read_followers(file_path= file_path)
        follow_array.remove(str(username))
        write_file(file_path,follow_array)
        return True
    except Exception as e:
        print(e)
        return False

def write_exception(alert):
    try:
        exception_file = open(base_expection_path+"alert.txt", "a")

    except Exception as e:
        exception_file = open(base_expection_path+"alert.txt", "w")

    exception_file.write(str(alert))
    exception_file.write(" TIME: ")
    exception_file.write(time.strftime("%D %H:%M", time.localtime(time.time())))
    exception_file.write('\n')
    exception_file.close()


def write_blacklist(username, bot):
    try:
        blacklist_file = open(base_path+"blacklist_usernames.txt","a")
        blacklistID_file = open(base_path+"blacklist.txt","a")

    except Exception:
        blacklist_file = open(base_path+"blacklist_username.txt","w")
        blacklistID_file = open(base_path+"blacklist.txt","w")
    finally:
        blacklist_file.write(str(username)+'\n')
        blacklistID_file.write(str(bot.get_userid_from_username(username))+'\n')
        blacklist_file.close()
        bot.add_blacklist(base_path+"blacklist.txt")

def read_username_blacklist():
    try:
        blacklist = open("blacklist_username.txt","r")
        user_list = []
        for name in blacklist:
            user_list.append(name)
        return user_list
    except Exception as e:
        write_exception(e)
        return []

def delete_hashtag(tag):
    try:
        hashtag_array = read_hashtags(file_path=base_path+hashtags_file)
        hashtag_array.remove(str(tag))
        write_file(file_path=base_path+hashtags_file,array=hashtag_array)
        return True
    except Exception:

        write_exception("trying to delete an unknown hashtag")
        return False


def append_to_black_list(bot,filepath):
    try:
        user_ids = read_followers(file_path=filepath)
        for ids in user_ids:
            write_blacklist(bot.get_username_from_userid(ids), bot)
    except Exception:
        write_exception("could append blacklits.")


def read_list_file(path):
    try:
        list_to_read = open(path, "r")
        empty_list = []
        for item in list_to_read :
            #this is needed t delete the space
            item = item.replace('\n', '')
            empty_list.append(item)
        return empty_list

    except Exception as e:
        write_exception(e)
        return []

def read_locations(filepath):

    try:
        arr = []
        locations = open(filepath, "r")
        for location in locations:
            arr.append(location)
        return arr
    except Exception:
        return []


def get_all_bot_users():
    ''' this will return a list of users with which the bot interacted '''
    try:
        followed = read_list_file(path="followed.txt")
    except Exception:
        followed = []
    try:
        skipped = read_list_file(path="skipped.txt")
    except Exception:
        skipped = []

    return list(followed + skipped)


def setup(bot):
    print("welcome to Mana growth instabot.... created by levesnworth")
    print("will run a few checks...")
    while True:
        print("is this a reboot? [y/n]")
        ans = input()
        if ans is 'y':
            return True

        elif ans is 'n':
            first_boot(bot)
            return False
        else:
            print("bad input try again")



def first_boot(bot):
    print("you want to freeze followers? press y if yes else whatever you like")
    ans = input()
    if ans is 'y':
        bot.freeze_following()

    print("do you wnat to unfollow non followers as to begin the account in clean?")
    ans = input()
    if ans is 'y':
        bot.unfollow_non_followers()
    print("all done !")



if __name__ == '__main__':
    print(read_followers(file_path=base_path+"follow.txt"))
