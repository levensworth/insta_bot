from file_helpers import *
def unfollow_all(bot):
    bot.unfollow_everyone()

def unfollow_non_followers(bot):
    bot.unfollow_non_followers()

def unfollow_from_file(bot,path ):
    unfollow_list = read_list_file(path)
    try:
        for user_id in unfollow_list:
            bot.unfollow(user_id)
    except Exception as e:
        write_exception(e)
        return False
