#!/bin/bash
awk '
BEGIN{
	out="Name||Projects||Drive Video Link\n";
	i=1;
}
!/^[ ]*$/ {
	if (i==1){
	gsub(/^[ \t]+|[ \t]+$/, "",$0);
	out = out$0"||"; i = 0;
	}
	else if($0!~/https:\/\/drive.google.com\/(file\/d|drive\/folders)\/[A-Za-z0-9_\-\/\?-_]*/ && i==0){
		gsub(/^[ \t]+|[ \t]+$/, "",$0);
		out = out$0" ";
	}
	else{
		gsub(/^[ \t]+|[ \t]+$/, "",$0);
		sub(/[ \t]+$/,"",out);
		out=out"||"$0"\n"; i = 1;
	}}
END{
printf("%s", out)}' $1 > csv
