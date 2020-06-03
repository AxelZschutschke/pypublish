#!/bin/bash

export resultFile=$1

function printLn()
{
	if [ $2 ]; then
		if [ "$resultFile" ]; then
			echo "," >> $resultFile
		else
			echo ","
		fi
	fi

	if [ "$resultFile" ]; then
		echo -n "$1" >> $resultFile
	else
		echo -n "$1"
	fi
}

function addSingle()
{
	printLn "   \"$1\": \"$2\"" $3
}

function addSubdict()
{
	printLn "   \"$1\": {" $3
	hadPredecessor=
	for i in $2; do
		subkey=$(echo $i | cut -f1 -d';')
		subvalue=$(echo $i | cut -f2 -d';')
		printLn "      \"$subkey\": \"$subvalue\"" $hadPredecessor
		hadPredecessor=true
	done
	printLn "   }"  
}

versions=$(dpkg -l | grep 'ii' | sed 's/ \+/;/g' | cut -f2,3 -d';' )

custom=""
if [ -f "$2" ]; then
    custom=$(cat $2 $3 $4 $5 | sed 's/\t/;/g')
fi

os=""
if [ -f /usr/bin/lsb_release ]; then 
    os=$(lsb_release -a 2>/dev/null |\
         grep "Description" |\
         sed 's/Description:[ \t]*\([^ \t]*\)/\1/g' )
fi

if [ -f /etc/os-release ]; then
    source /etc/os-release
    os=$PRETTY_NAME
fi

echo -n "" > $resultFile
printLn "{"
addSingle "type" "Linux"
addSingle "os" "$os" true
addSingle "kernel" "$(uname -r)" true
addSingle "platform" "$(uname -i)" true
addSingle "host" "$(hostname)" true
addSingle "dnsname" "$(dnsdomainname)" true
addSingle "user" "$(whoami)" true
if [ "$custom" ]; then
    addSubdict "custom" "$custom" true
fi
addSubdict "packages" "$versions" true
printLn "}"
