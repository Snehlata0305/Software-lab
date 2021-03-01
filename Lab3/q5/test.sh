#!/bin/bash

rm -f csv
./q5.sh testcase/input/input1
diff -Z testcase/output/output1 csv > result
if [[ -s result ]];
then
	echo failed
else
	echo passed
fi
rm result