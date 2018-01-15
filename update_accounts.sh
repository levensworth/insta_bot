#!/bin/bash
#files=("$@")
files=("formagge" "companiademascotasok" "360eyewear" "borja" "fedediazparta" "bpstudio96" "fernandolema" " managrowth")
files_to_cpy=("comment.py" "follow.py" "unfollow.py" "file_bot.py" "file_helpers.py" "like.py" "mailer.py" "stats.py")
for user in "${files[@]}"
do
    for file in "${files_to_cpy[@]}"
    do
        cp "${file}"  "../${user}"
    done
done
