#! /bin/bash

filename='q4_in.txt'

while read line; do
read -a num <<< $line
done < $filename

tot=${#num[@]}
sum=0

for i in "${num[@]}"; do
 sum=$(echo "scale=2; $sum+$i" | bc)
done

 mean=$(echo "scale=2; $sum/$tot" | bc)
echo $mean

for ((i = 0; i<tot; i++)) do
 for((j = 0; j<tot-i-1; j++)) do
  if (( $(echo "${num[j]} > ${num[$((j+1))]}" |bc -l) ));
    then
     temp=${num[j]} 
     num[$j]=${num[$((j+1))]}   
     num[$((j+1))]=$temp 
  fi
 done
done

if [ $((tot%2)) -eq 0 ]
 then
  ind=$((tot/2))
  a=${num[ind]}
  b=${num[$((ind-1))]}
  medsum=$(echo "scale=2; $a+$b" | bc)
  res=$(echo "scale=2; $medsum/2" | bc)
  echo $res
  #echo $((((a+b))/2))
 else
  echo ${num[$((tot/2))]}
fi
