rm -f tempout
rm -f dump
python3 main.py > tempout 2> dump
diff -Z tempout output > result
if [[ -s result ]];
then
    echo "failed"
else 
    echo "passed"
fi
rm -f result dump tempout