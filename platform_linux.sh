#!/bin/bash

export resultFile=$1

function printLn()
{
	if [ "$resultFile" ]; then
		$1 > $resultFile
	else
		echo $1
	fi
}

function addSingle()
{
	printLn "   \"$1\": \"$2\""
}

function addSubdict()
{
	printLn "   \"$1\": {"
	for i in $2; do
		subkey=$(echo $i | cut -f1 -d';')
		subvalue=$(echo $i | cut -f2 -d';')
		printLn "      \"$subkey\": \"$subvalue\""
	done
	printLn "   }"  
}

versions=$(dpkg -l | grep 'ii' | sed 's/ \+/;/g' | cut -f2,3 -d';' )
os=$(lsb_release -a 2>/dev/null |\
	 grep "Description" |\
	 sed 's/Description:[ \t]*\([^ \t]*\)/\1/g' )

printLn "{"
addSingle "os" ""
addSingle "kernel" "$(uname -r)"
addSingle "platform" "$(uname -i)"
addSingle "host" "$(hostname)"
addSingle "user" "$(whoami)"
addSubdict "packages" "$versions"
printLn "}"
