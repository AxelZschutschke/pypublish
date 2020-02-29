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
os=$(lsb_release -a 2>/dev/null |\
	 grep "Description" |\
	 sed 's/Description:[ \t]*\([^ \t]*\)/\1/g' )

echo -n "" > $resultFile
printLn "{"
addSingle "type" "Linux"
addSingle "os" "$os" true
addSingle "kernel" "$(uname -r)" true
addSingle "platform" "$(uname -i)" true
addSingle "host" "$(hostname)" true
addSingle "user" "$(whoami)" true
addSubdict "packages" "$versions" true
printLn "}"
