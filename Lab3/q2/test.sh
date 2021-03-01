rm -f url
./q2.sh testcase/input/input1
diff -Z testcase/output/output1 url > result
if [[ -s result ]];
then
	echo failed
else
	echo passed
fi

rm result

diff -Z testcase/input/input1 testcase/input/input1_cleaned > result
if [[ -s result ]];
then
	echo failed
else
	echo passed
fi

rm result
