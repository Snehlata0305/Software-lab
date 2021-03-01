#! /bin/bash

cp $1 temp.txt
while IFS= read line; do
 sed -i "s/\b"$line"\b/bleep/gI" temp.txt
done < $2
echo "$(<temp.txt)"
rm temp.txt
