import csv
import time
base_path = "./storage/"
base_expection_path = "./alerts/"

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
    return file_dict


def read_followers(file_path):
    file_array = csv.reader(open(file_path,"r"))
    arr = []
    for line in file_array:
        arr.append(line[0])

    return arr

def read_hashtags(file_path):
    file_array = csv.reader(open(file_path,"r"))
    arr = []
    for line in file_array:
        arr.append(line[0])

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

def wirte_exception(alert):
    try:
        exception_file = open(base_expection_path+"alert.txt", "a")

    except Exception as e:
        exception_file = open(base_expection_path+"alert.txt", "w")

    exception_file.write(alert + " TIME: "+ time.strftime("%D %H:%M", time.localtime(time.time())))
    exception_file.write('\n')
    exception_file.close()


def write_balcklist(username, bot):
    try:
        blacklist_file = open(base_path+"balcklist_usernames.txt","a")
        blacklistID_file = open(base_path+"balcklist.txt","a")

    except Exception:
        blacklist_file = open(base_path+"balcklist_username.txt","w")
        blacklistID_file = open(base_path+"balcklist.txt","w")
    finally:
        blacklist_file.write(str(username)+'\n')
        blacklistID_file.write(str(bot.get_userid_from_username(username))+'\n')
        blacklist_file.close()


def delete_hashtag(tag):
    try:
        hashtag_array = read_hashtags(file_path=base_path+hashtags_file)
        hashtag_array.remove(str(tag))
        write_file(file_path=base_path+hashtags_file,array=hashtag_array)
        return True
    except Exception:

        write_exception("trying to delete an unknown hashtag")
        return False



if __name__ == '__main__':
    write_balcklist("tu vieja")
