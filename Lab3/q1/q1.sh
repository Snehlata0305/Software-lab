#!/bin/bash

awk -F"!" '
x=0;
y=0;
{ for (i = 1; i <= NF; i++)
	{ split ( $i, b,"-" )
	if(b[1]=="L"){
	x=x-b[2];
	print "L\t(" x "," y")";}
	else if(b[1]=="R"){
	x=x+b[2];
	print "R\t(" x "," y")";}
	else if(b[1]=="U"){
	y=y-b[2];
	print "U\t(" x "," y")";}
	else if(b[1]=="D"){
	y=y+b[2];
	print "D\t(" x "," y")";}
	}
print "Final Position: (",x,y")","\n"; }
' $1 >out01
