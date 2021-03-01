python3 q7.py testcase/input.txt > out

diff -Z testcase/output.txt out > result

if [[ -s result ]];
then
	echo failed
else
	echo passed
fi
rm out result