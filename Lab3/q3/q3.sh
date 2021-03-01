#! /bin/bash
awk '/[a-zA-z]+[-][0-9][0-9][0-9][-][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/{for(i=1;i<=NF;++i)if($i~/[a-zA-z]+[-][0-9][0-9][0-9][-][0-9][0-9][0-9][0-9][0-9][0-9][0-9][0-9]/)print (i==1?"":" ")$i(i==NF?"":" ")}' OFS=' ' $1 > abc.txt
echo "$(awk -F"-" '$3 ~ "^[0-9][0-9]*[ ]*$" && $3!~"^0*[ ]*$" {print $0}' abc.txt)" > abc.txt
sed -i 's/-/,/g' abc.txt

sed -e 's/\t\+/,/g' -e 's/ ,/,/g' STD_Codes_list > text.txt
echo "$(awk -F',' 'NR==FNR{city[$1]=$2; state[$1]=$3; key[$1]=1;next;} {print $0,(key[$2]==1? city[$2]:" t"),(key[$2]==1? state[$2]:" t")}' OFS=', ' text.txt abc.txt)" > abc.txt
sed -e 's/,/ /' -e 's/,/-/' -e 's/,//' abc.txt
rm abc.txt
rm text.txt
