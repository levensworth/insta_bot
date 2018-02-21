from file_helpers import *
unfollow_file = "unfollow.txt"
blacklist_file = "storage/blacklist.txt"

def unfollow_all(bot):
    bot.unfollow_everyone()

def unfollow_non_followers(bot):
    bot.unfollow_non_followers()
    update_blacklist(bot,unfollow_file)

def unfollow_interacted_users(bot,path ):
    unfollow_list = get_all_bot_users()
    try:
        for user in unfollow_list:
            while not bot.unfollow(user):
                pass
        
        for user_id in unfollow_list:
            write_blacklist(username=bot.get_username_from_userid(str(user_id)), bot=bot)

        update_blacklist(unfollow_file=unfollow_file)
        bot.add_blacklist(blacklist_file)
    except Exception as e:
        write_exception(str(e) + " from unfollow_interacted_users")
        return False

def update_blacklist(bot, unfollow_file):
    user_ids =  read_dict_file(file_path=unfollow_file)
    for uid in user_ids:
        write_blacklist(username=bot.get_username_from_userid(uid), bot=bot)

    bot.add_blacklist(blacklist_file)
