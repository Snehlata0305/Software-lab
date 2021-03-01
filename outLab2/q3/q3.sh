#! /bin/bash

pathdtl=$1
cntnum=$(grep -hcve '^$' $(find $pathdtl/ -name '*' -type f -print))

num=($cntnum)

tot=${#num[@]}
sum=0

for i in "${num[@]}"; do
 sum=$((sum+i))
done

echo $sum
