#!/bin/bash
RESULTS_FOLDER=$1
TEST_COUNT=$2
NUMBER_OF_ITERATIONS=$3

if [ $# -ne 3 ]; then
    echo "Must provide precisely two arguments.  The first argument is a folder name to place the results in, \
          the second argument is the number of this test. The third argument is the number of trials to run per test."
    exit 1
fi


spinner()
{
    local pid=$1
    local delay=500000
    local spinstr='|/-\'
    while [ "$(ps | awk '{print $1}' | grep $pid)" ]; do
        local temp=${spinstr#?}
        printf " [%c]  " "$spinstr"
        #printf "                                                [%c]  " "$spinstr"
        local spinstr=$temp${spinstr%"$temp"}
        usleep $delay
        #printf "\b\b\b\b\b\b"
        printf "\r"
    done
    printf "    \b\b\b\b"
}

#if [ -d "$RESULTS_FOLDER" ]; then #if folder exists already...
#  if [ "$(ls -A $RESULTS_FOLDER)" ]; then #directory is not empty
#     echo -n "Your results folder is not empty. Data may be overwritten. Continue? y/n "
#	 read response
#	 while true
#	 do
#	 	if  [ "$response" == "y" ]; then
#  			echo -n "Continuing..."
#   		wait 1
#  			break
#	 	elif [ "$response" == "n" ]; then
#  			echo -n "Program exiting..."
#  			exit 1
#  		else
#  			echo -n "Invalid response. Please respond with \"y\" for yes or \"n\" for no."
#  			read response
#  	 	fi
#	done
#  else
#     echo "$RESULTS_FOLDER is Empty"
#     wait 1
#  fi
#fi

mainTask()
{
COUNTER=1
echo -ne "       Test #$TEST_COUNT: 0/"$NUMBER_OF_ITERATIONS" trials complete."
echo -ne "\r"
while true
do
  ./get_rssi 2&>/dev/null
  #./example &
  wait

  mkdir -p "./""$RESULTS_FOLDER""/""$TEST_COUNT"
  mv rssi_agg.csv ./"$RESULTS_FOLDER"/"$TEST_COUNT"/"$TEST_COUNT"_"$COUNTER".csv
  mv output.txt ./"$RESULTS_FOLDER"/"$TEST_COUNT"/"$TEST_COUNT"_"$COUNTER".txt

  CSVFILE="./""$RESULTS_FOLDER""/""$TEST_COUNT""/""$TEST_COUNT""_""$COUNTER"
  TXTFILE="./""$RESULTS_FOLDER""/""$TEST_COUNT""/""$TEST_COUNT""_""$COUNTER"


  grep '159113607448223\|159113606651491\|278020541036329' "$CSVFILE".csv  > "$CSVFILE"_GREPPED.csv
  grep -A 1 '90:B6:86:0D:06:9F\|90:B6:86:00:DE:63\|FC:DB:B3:96:B7:29' "$TXTFILE".txt > "$TXTFILE"_GREPPED.txt
  #Order: My edison, Monica's eddie, Eduardo
  touch ./"$RESULTS_FOLDER"/f133q13.temp
  grep -v "\-\-" "$TXTFILE"_GREPPED.txt > ./"$RESULTS_FOLDER"/f133q13.temp
  mv ./"$RESULTS_FOLDER"/f133q13.temp "$TXTFILE"_GREPPED.txt

  echo -ne " Test #$TEST_COUNT: "$COUNTER"/"$NUMBER_OF_ITERATIONS" trials complete."
  if [[ $(($COUNTER + 1))  -le $NUMBER_OF_ITERATIONS ]]
  then
    echo -ne "\r"
  else
    :
  fi

  if [ "$COUNTER" -eq "$NUMBER_OF_ITERATIONS" ]; then
    break;
  fi

  COUNTER=$((COUNTER+1))
done
echo -e "\n"

#echo All jobs done $COUNT
}

secondaryTask()
{
    sleep 10
}

(mainTask) &
#(secondaryTask) &
spinner $!
