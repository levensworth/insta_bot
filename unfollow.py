from file_helpers import *
unfollow_file = "unfollow.txt"
blacklist_file = "storage/blacklist.txt"

def unfollow_all(bot):
    bot.unfollow_everyone()

def unfollow_non_followers(bot):
    bot.unfollow_non_followers()
    update_blacklist(bot,unfollow_file)

def unfollow_from_file(bot,path ):
    unfollow_list = read_list_file(path)
    try:
        bot.unfollow_users(unfollow_list)
        for user_id in unfollow_list:
            write_blacklist(username=bot.get_username_from_userid(str(user_id)), bot=bot)

        bot.add_blacklist(blacklist_file)
    except Exception as e:
        write_exception(str(e) + " from unfollow_from_file")
        return False

def update_blacklist(bot, unfollow_file):
    user_ids =  read_dict_file(file_path=unfollow_file)
    for uid in user_ids:
        write_blacklist(username=bot.get_username_from_userid(uid), bot=bot)

    bot.add_blacklist(blacklist_file)
