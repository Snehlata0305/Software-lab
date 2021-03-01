#! /bin/bash

ipfile=$1
timein=$2
timeout=$3

#remove header
sed '1d' $ipfile > tmpfl
sed -E -i 's/\t[0-9][0-9]\/[0-9][0-9]\/[0-9]{4},\s/\t/g' tmpfl

#remove out01 if exits
if [ -f "out01" ]; then
 rm out01
fi

#seperating columns using awk
IFS="$"
nmline=($(awk -F '\t' '{print $1}' tmpfl | sort -u))
col1in=($(awk -F '\t' '{print $1}' tmpfl))
col2in=($(awk -F '\t' '{print $2}' tmpfl))
col3in=($(awk -F '\t' '{print $3}' tmpfl))

#splitting to array
readarray -t <<<$col1in
col1arr=("${MAPFILE[@]}")
readarray -t <<<$col2in
col2arr=("${MAPFILE[@]}")
readarray -t <<<$col3in
col3arr=("${MAPFILE[@]}")

#unique names
readarray -t <<<$nmline
arr=("${MAPFILE[@]}")

#number of students and number of entries
nline=(${#col1arr[@]})
nstd=(${#arr[@]})

#set all to N - Not Visited
for ((x=0;  x<$nline; x++)); do
flg[$x]="N"
done

#setting timein to meeting start time if lesser
for ((q=0;  q<$nline; q++)); do
  tin=$(date -u -d "${col3arr[$q]}" +"%s")
  tstart=$(date -u -d "$timein" +"%s")
  if [[ "$tin" < "$tstart" ]]; then
    col3arr[$q]=$timein
   fi
done

for ((p=0;  p<$nstd; p++)); do
 person=${arr[p]}
 tot=0;
 for ((q=0;  q<$nline; q++)); do
  if [[ "${col1arr[q]}" == "$person" && "${col2arr[q]}" == "Joined" && "${flg[q]}" == "N" ]]; then
   tin1=$(date -u -d "${col3arr[$q]}" +"%s")
   flg[q]="Y"
   for ((w=q+1;  w<$nline; w++)); do
    if [[ "${col1arr[w]}" == "$person" && "${col2arr[w]}" == "Left" && "${flg[w]}" == "N" ]]; then
     tout1=$(date -u -d "${col3arr[$w]}" +"%s")
     tdiff=$((tout1-tin1))
     tot=$((tot+tdiff))
     flg[w]="Y"
     break
    else
     tout1=$(date -u -d "$timeout" +"%s")
     tdiff=$((tout1-tin1))
     tot=$((tot+tdiff))
     break
    fi
   done
  fi
  done
  
  hr=$((tot/3600))
  tmin=$((tot%3600))
  min=$((tmin/60))
  sec=$((tmin%60))
  #make 2 digits
  if [ $hr -le 9 ];then hr=0$hr;fi
  if [ $min -le 9 ];then min=0$min;fi
  if [ $sec -le 9 ];then sec=0$sec;fi

  echo -e $person'\t'$hr':'$min':'$sec >> out01
done

rm tmpfl
