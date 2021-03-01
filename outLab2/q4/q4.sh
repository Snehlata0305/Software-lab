#! /bin/bash

a=$(wc -l < actual_output.txt)
grep -Fxvf actual_output.txt generated_output.txt > temp.txt
g=$(wc -l < temp.txt)
rm temp.txt
echo "Secured $((a-g)) marks out of $((a))"
