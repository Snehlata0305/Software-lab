./q3.sh testcase/input3 > out

diff -Z testcase/output3 out > result

if [[ -s result ]];
then
	echo failed
else
	echo passed
fi
rm out result