#NOTE: Average option does NOT work as of yet, please do not enable

import os, sys, time, csv, getopt, re, operator #for sort
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

				numbers = match.group(0).split("_")
                                n2 = numbers[0].split("/")
                    
				#finalRow = newRow0 + newRow1 + newRow2 + [match.group(0)] 
				#****finalRow = newRow0 + newRow1 + newRow2 + [numbers[0]] + [numbers[1]]
				                                         #test number    #trial number (a single test has multiple trials averaged together) 
				#note: newRow[0-2] are comprised of three entries each, [] is placed around numbers to make it into a row object
                                finalRow = newRow0 + newRow1 + newRow2 + [n2[1]] + [numbers[1]]

				log.append(finalRow)
			i += 1


output = OPTIONS["output"] + "." + OPTIONS["extension"].lower()

allTruncRows = []
with open(output, "w") as file:
	writer = csv.writer(file)
	for entry in log:                                       # Original: [2], [5], [8], [9]
		truncRow = [entry[1], entry[4], entry[7], entry[9], entry[10]] #change to [1], [4], [7] to get signal level instead of RSSI (quality)
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
	
        #print (allTruncRows)
        #list1 = sorted(allTruncRows, key=operator.itemgetter(3,4))
        #print (list1)
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
