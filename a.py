import os, sys, time, csv, getopt, re
from datetime import datetime

'''
Message CSV Parser (mcp.py) parses message CSV files with format: sender, [garbage], date, message.
At minimum, a file (-f filename) or directory (-d dirname) must be provided.
Options:
The program is built to be robust, and therefore can take command line options.
--file (-f), the 
--dir (-d), the folder
--output (-o), sql,csv,txt
--raw (-r): along with removing newlines and trailing spaces, remove all characters not in the set[a-z0-9]
'''

#https://stackoverflow.com/questions/3041986/apt-command-line-interface-like-yes-no-input
def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")

def get_number_of_runs(typeOfRun, softUpperLimit, hardUpperLimit,):
#https://docs.python.org/3/tutorial/errors.html
	while True:
		try:
			numberOfRuns = int(raw_input("How many " + typeOfRun + "s would you like to run? "))
			if (numberOfRuns >= softUpperLimit and numberOfRuns < hardUpperLimit):
				keepGoing = query_yes_no("Are sure you want to run that many " + typeOfRun + "s?", None)
				if keepGoing:
					return numberOfRuns
			elif (numberOfRuns < 1 or numberOfRuns >= hardUpperLimit):
				print("That's an invalid number of " + typeOfRun + "s.  Please pick a number in the range [1-" + str(hardUpperLimit - 1) + "].")
			else:
				return numberOfRuns

		except ValueError:
			print("Please type in a valid number.")
		


numberOfTests = get_number_of_runs("test", 101, 1001)
numberOfTrials = get_number_of_runs("trial", 11, 51)
nameOfDataSet = raw_input("What would you like to name this data set? (please do not use spaces): ").lower().replace(" ", "")

print("Ready to begin tests. Please move to your first location.")
time.sleep(2)
choice = raw_input("When ready, hit enter to begin. ").lower()
while True:
	if choice == '':
		break
	elif choice == 'q' or choice == 'quit':
		print("Exiting program...")
		exit(0)
	else:
		choice = raw_input("Invalid Command. Please hit enter to begin testing (or \"quit\" to quit). ").lower()
		#raw_input("Hit enter or type in \"go\" to begin. ")

currentTestNumber = 1
while (currentTestNumber <= numberOfTests):
	os.system("./multi.sh " + str(nameOfDataSet) + "_TEMP " + str(currentTestNumber) + " " + str(numberOfTrials))
	print("Test number " + str(currentTestNumber) + " completed!\n")
	time.sleep(1)
	if (currentTestNumber == numberOfTests):
		choice = raw_input("Hit enter to process your completed tests, \"r\" to rerun the last test, or \"quit\" to quit. ").lower()
	else:
		choice = raw_input("Please move to the next position and hit go when ready. Or, to rerun the last test, type in \"r\". ").lower()
	while True:
		if choice == '':
			currentTestNumber +=1
			break
		elif choice == 'r':
			break
		elif choice == 'q' or choice == 'quit':
			if (currentTestNumber == numberOfTests):
				print("Exiting program without additional test processing...")
			else:
				print("Exiting program early...")
			exit(0)
		else:
			if (currentTestNumber == numberOfTests):
				choice = raw_input("Invalid Command. Please hit enter to process the completed tests, \"r\" to rerun the last "
				                   "test, or \"quit\" to quit. ").lower()
			else:
				choice = raw_input("Invalid Command. Please hit enter to begin testing, \"r\" to rerun the last test, or \"quit\" to quit. ").lower()
print("All tests processed")

os.system("./movingScript.sh " + str(nameOfDataSet) + "_TEMP " + str(nameOfDataSet) + "_Results")
print("All tests moved to final processing folder.")
#if not (numberOfTests.isdigit()):
#	print("Not a digit")

'''
#command line options
OPT_DESCRIPTIONS = {
	"help, h": "Prints this information.",
	"file, f": "The path to a file to be parsed.",
	"dir, d": "A directory of files to be parsed. Subdirectories will also be parsed.",
	"extension, e": "csv (default), sql",
	"output, o": "The path of the output file. Defaults to ./merge.EXTENSION"
}
OPTIONS = {
	"file": None,
	"dir": None,
	"extension": "csv",
	"output": "./merge",
	"average": None,
	"help": False
}
SHORT_OPTION_MAP = {"f": "file", "d": "dir", "o": "output", "e": "extension", "a": "average", "h": "help"}

#todo: what happens when uncessary options are provided
#obtaining and formatting options passed to program
shortopts, longopts = "h", ["help"]
for short, long in SHORT_OPTION_MAP.items():
	if not long == 'average':
		longopts.append(long + "=")
	else:   #don't want a required argument for the "average" option
		longopts.append(long)
	if not short == 'a':
		shortopts += (short + ": ")
	else:
		shortopts += (short + " ")  #don't want a required argument for the "average" option

#print(longopts)
#print(shortopts)

optionTuples = getopt.getopt(sys.argv[1:], shortopts, longopts)
#print(optionTuples)

for pair in optionTuples[0]:
	option, value = pair[0].lstrip("-"), pair[1]
	option = SHORT_OPTION_MAP[option] if (len(option) == 1) else option
	if option not in OPTIONS:
		print("You have provided an unnecessary option/value pair: " + str((option, value)))
		sys.exit(2)
	else:
		OPTIONS[option] = value

if (OPTIONS["help"] != False):
	helpText = "Message CSV Parser (mcp.py) parses message CSV files with format: sender, [garbage], date, message.\nAt minimum, a file (-f filename) or directory (-d dirname) must be provided.\n\n"
	for option, text in OPT_DESCRIPTIONS.items():
		helpText = helpText + "\t" + (option + ": ").ljust(15) + text + "\n"
	print(helpText)
	exit(0)


if (OPTIONS["file"] == None) and (OPTIONS["dir"] == None):
	print("You must provide either a file or directory to be processed.")
	sys.exit(1)
elif (OPTIONS["file"] != None) and (OPTIONS["dir"] != None):
	#choosing the option which was set last
	opts = sys.argv[1:]
	opts.reverse()
	if (opts.index(OPTIONS["file"]) < opts.index(OPTIONS["dir"])): #should really be looking for keys, not values
		OPTIONS["dir"] = None
	else:
		OPTIONS["file"] = None


#https://stackoverflow.com/questions/6382804/how-to-use-getopt-optarg-in-python-how-to-shift-arguments-if-too-many-arguments
optionTuples, arg = getopt.getopt(sys.argv[1:], shortopts, longopts)  #why does it make the difference b/w working and not working if I include the ", arg" in the assignment???
averageResults = False
for opt, arg in optionTuples:
	if opt in ('-a', '--average'):
		averageResults = True


def createFileList(dir): return [dir + "/" + fn for fn in os.listdir(dir)]
#doing the actual work
filenames = [OPTIONS["file"]] if (OPTIONS["file"] != None) else createFileList(OPTIONS["dir"])
log = []
for filename in filenames:
	#skipping over non-csv files
	if (len(filename) < 3 or filename[-3:].lower() != "csv"):
		continue
	#print(filename)
	with open(filename) as csvFile:
		reader = csv.reader(csvFile)
		#print(filename)   #debugging
		i = 0
		for row in reader:
			#Keep a consistent ordering of cells/AP nodes within a row
			#To-do: Handle error cases if there are not exactly 3 rows in the file (e.g. data set 1 #30)
			if (row[0] == "278020541036329"):
				newRow1 = row
			elif (row[0] == "159113607448223"):
				newRow0 = row
			elif (row[0] == "159113606651491"):
				newRow2 = row
			if ((i + 1) % 3 == 0):
				match = re.search('(?<=_).*?(?=_GREPPED)', filename) #regex, match the expression between "_" and "GREPPED"
				                                                     #in the filename string
				#testMatch = re.search('(?<=_).*?(?=_[0-9]+_GREPPED)', filename) #regex, match the expression between "_" and "_#_GREPPED"
				#trialMatch = re.search('(?<=_[0-9]+_).*?(?=_GREPPED)', filename) #regex, match the expression between "DataSet_#_" and "_GREPPED"

				#See: http://stackoverflow.com/questions/6109882/regex-match-all-characters-between-two-strings
				#https://docs.python.org/2/library/re.html --> Explaination on match.group(0) --> (group0() returns the ENTIRE matched pattern)
				#http://pythex.org/?regex=(%3F%3C%3D_).*%3F(%3F%3DGREPPED)&test_string=results%2F2DataSet_9GREPPED.csv&ignorecase=0&multiline=0&dotall=0&verbose=0
				#if match:
				#	print(match.group(0))

				numbers = match.group(0).split("_")

				#finalRow = newRow0 + newRow1 + newRow2 + [match.group(0)] 
				finalRow = newRow0 + newRow1 + newRow2 + [numbers[0]] + [numbers[1]]
				                                         #test number    #trial number (a single test has multiple trials averaged together) 
				#note: newRow[0-2] are comprised of three entries each, [] is placed around numbers to make it into a row object

				#finalRow[9] = finalRow[9].replace("_", "")

				#print(finalRow)
				log.append(finalRow)
			i += 1

			#if i % 3 == 0:
			#	newRow1 = row
				#print(newRow1)
				#print("1")
			#elif i % 3 == 1:
			#	newRow2 = row
				#print(newRow2)
				#print("2")
			#else:
			#	newRow2 = newRow1 + newRow2 + row
			#	print(newRow2)
				#print("3")
			#i += 1
			# http://stackoverflow.com/questions/24861673/merge-two-rows-in-a-csv-file-in-python
			#log = row + 1
			#print(log)
			#row += 2
		#data = list(reader)
    	#row_count = len(data)
    	#if (row_count < 3):
    	#	print("CSV file " + filename + " does not have at least 3 rows.\n")
    	#	sys.exit(2)
    	#for row in reader:
			#log = (row + 2) + (row + 1) + row
		#	log = row
		#	print(log)
		#	row += 2

output = OPTIONS["output"] + "." + OPTIONS["extension"].lower()
#output = OPTIONS["extension"].lower()

allTruncRows = []
#with open(OPTIONS["output"], "w") as file:
with open(output, "w") as file:
	writer = csv.writer(file)
	for entry in log:                                       # Original: [2], [5], [8], [9]
		truncRow = [entry[2], entry[5], entry[8], entry[9], entry[10]] #change to [1], [4], [7] to get signal level instead of RSSI (quality)
		                                                    #this data is in the format of one of the GREPPED files, with everything in a single
		                                                    #row (instead of displayed over three rows), with an additional column appended for the
		                                                    #test number
		                                                    #Thus, an entry looks like the following:
		                                                    #15...223, -x dBm, x/70 RSSI, 278..., -x dBm, x/70 RSSI, 159...491, -x dBm, x/70 RSSI, test #
		                                                    #    [0]    [1]       [2]      [3]      [4]      [5]        [6]       [7]     [8]        [9]
		if averageResults is False:
			writer.writerow(truncRow)
		else:
			allTruncRows.append(truncRow)

	if averageResults is False:
		sys.exit(0)
	
	#continue on with logic for when we're averaging the results
	counter = 1
	summedRow = [int(allTruncRows[0][0]), int(allTruncRows[0][1]), int(allTruncRows[0][2]), int(allTruncRows[0][3])]
	for prevEntry, entry in zip(allTruncRows, allTruncRows[1:]):
		#numberOfDigits = len(str(truncRow[3]))
		if prevEntry[3] == entry[3]:
			counter += 1
			summedRow[0] += int(entry[0])
			summedRow[1] += int(entry[1])
			summedRow[2] += int(entry[2])
		else:
			summedRow[0] /= counter
			summedRow[1] /= counter
			summedRow[2] /= counter
			writer.writerow(summedRow)
			summedRow = [int(entry[0]), int(entry[1]), int(entry[2]), int(entry[3])]
			counter = 1
	if allTruncRows[-1][3] == allTruncRows[-2][3]: #the last row was from the same test as the second to last row
		summedRow[0] /= counter
		summedRow[1] /= counter
		summedRow[2] /= counter
		writer.writerow(summedRow)
	else: #the last row was a separate test from the second to last row; and thus that last test had only one trial
		writer.writerow(summedRow)

			

	#writer = csv.DictWriter(file, ["sender", "date", "text"], quoting = csv.QUOTE_ALL)
	#for message in messageLog:
	#	writer.writerow(message.dict()) + message.text + '"'))



#for filename in os.listdir(directory):
#    if filename.endswith(".asm") or filename.endswith(".py"): 
#        # print(os.path.join(directory, filename))
#        continue
#    else:
#        continue


'''
