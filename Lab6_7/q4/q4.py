#!/usr/bin/env python3

from stackapi import StackAPI
import csv

input_string = input()
tagip = input_string.strip().replace(" ",";")

SITE = StackAPI('stackoverflow')
SITE.page_size = 50
SITE.max_pages = 5
questions = SITE.fetch('questions', tagged=tagip, sort='votes')

usertag=tagip.lower().replace(";","_")
arrtag=usertag.split("_")

cnt=0
dictnew = {}
listfinal = []
for k in questions["items"]:
	flgval = 1
	if "accepted_answer_id" in k.keys(): #if k.keys has accepted_answer_id then proceed, also check if all tags are present
		for tval in arrtag:
			if tval not in k["tags"]:
				flgval=0
		if flgval == 1:
			dictnew["question_id"]=k["question_id"]
			dictnew["tag"]= usertag
			dictnew["link"]=k["link"]
			dictnew["tags"]=k["tags"]
			dictnew["accepted_answer"]=k["link"]+"/#"+str(k["accepted_answer_id"])
			listfinal.append(dictnew.copy())
			cnt+=1
			if cnt >= 50:
				break

csvfile = usertag+".csv"
keyvals = ['question_id', 'tag', 'link', 'tags', 'accepted_answer']
with open(csvfile,"w") as file:
    dict_writer = csv.DictWriter(file, keyvals)
    dict_writer.writeheader()
    dict_writer.writerows(listfinal)
