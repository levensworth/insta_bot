
from file_helpers import *
from shutil import *


def transfer_all_files(list_of_files=[], root_dest="."):
    for f in list_of_files:
        copyfile(f, "../"+root_dest+"/"+f)


accounts = read_list_file("../accounts.txt")
files_to_cpy=["comment.py" ,"follow.py" ,"unfollow.py" ,"file_bot.py" ,"file_helpers.py" ,"like.py" ,"mailer.py" ,"stats.py"]
for account in accounts:
    transfer_all_files(files_to_cpy, account)
print("done")
