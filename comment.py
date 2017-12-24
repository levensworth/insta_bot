def comment_timeline(bot,timeline_comment_path, timeline_comment_number ):
    medias = bot.get_timeline_medias()
    try:
        for media in medias:
            bot.comment(media_id=media, comment_text=get_random_timeline_comment(timeline_comment_path, timeline_comment_number))
        return True

    except Exception as e:
        print(e)
        return False

def get_random_timeline_comment( path, timeline_comment_number):
    try:
        comment_file = open(path, 'r')

        index = 1
        length = random.randrange(1,timeline_comment_number)
        for comment in comment_file:
            if index == length:
                return str(comment)
            index = index + 1
    except Exception as e:
        write_exception('an error ocurred while trying to read the time_line comments file')
