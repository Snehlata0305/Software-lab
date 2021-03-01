#! /bin/bash

ipfile=$1

sed -i -e 's/\t/ /g' -e 's/\s\s*/ /g' $ipfile

awk 'gsub(" ","\n",$0)' $ipfile > outtmp
awk 'match($0,/http[s]?:\/\/www\.cse\.iitb\.ac\.in\/~[a-z]*/) {print substr($0,RSTART,RLENGTH)}' outtmp > url
rm outtmp

sed -E -i 's/\(([^@^ ]*\.(com|in|org|net|co|us|edu|gov|au)[^\)^ ]*)\)/\( \1 \)/g' $ipfile
sed -E -i -e 's/http[s]?\:\/\/[^ ]*//g' -e 's/(^|\s)[^@^ ]*\.(com|in|org|net|co|us|edu|gov|au)[^@^ ]*(\s|$)/ /g' $ipfile
sed -i -e 's/\t/ /g' -e 's/\s\s*/ /g' $ipfile
