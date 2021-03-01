#!/bin/bash
a="$1"
s=0
x=0
for ((i=1;i<=$((a));i++)); do
	x=$((i*i))
	s=$((s+x))
done
echo "$s"
