#! /usr/bin/awk -f

BEGIN {marks=0;}
NR==FNR{outs[$1]=$0; key[$1]=1; next;}
{ if(key[$1]==1)
 {n=split($0,actual," "); 
 m=split(outs[$1],obtained," "); 
  for(i=2; i<=m;i++)
  { if(actual[i]==obtained[i]) {marks++;} }
 }
 }
 END{ print marks;}
