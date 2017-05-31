#!/bin/bash

ONE_FOLDER_TO_PROCESS=$1
FINAL_FOLDER=$2

#Check for correct command line arguments
if [ $# -ne 2 ]; then
    echo "Must provide precisely three arguments"
    exit 1
fi

if [ ! -d "$ONE_FOLDER_TO_PROCESS" ]; then
	echo "Directory 1 does not exist! Program exiting..."
	exit 1
fi

mkdir -p "$FINAL_FOLDER"
#if [ ! -d "$FINAL_FOLDER" ]; then
#	echo "Results directory does not exist! Program exiting..."
#	exit 1
#fi


ls $ONE_FOLDER_TO_PROCESS > contentTEMP.temp
numberOfFiles=`wc -l < contentTEMP.temp`
COUNTER=1

while read DIRNAME
do
	ls $ONE_FOLDER_TO_PROCESS"/"$DIRNAME | grep 'GREPPED.csv' > subContentTEMP.temp
	while read FILENAME
	do
		cp $ONE_FOLDER_TO_PROCESS"/"$DIRNAME"/"$FILENAME $FINAL_FOLDER"/"$FILENAME
		#echo -ne "Processing Folder 1: "$COUNTER"/"$numberOfFiles" files complete."
		#if [[ $(($COUNTER + 1))  -le $numberOfFiles ]]
		#then
		#	echo -ne "\r"
		#else
		#	:
		#fi
		COUNTER=$((COUNTER+1))
	done < subContentTEMP.temp
	rm subContentTEMP.temp

done < contentTEMP.temp
echo -ne "\nFolder 1 processing complete!\n"

rm contentTEMP.temp
