import os, sys, time, csv, getopt, re, shutil
from datetime import datetime


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
while (os.path.isdir(nameOfDataSet + "_TEMP")):
        keepGoing = query_yes_no("A directory for that data set already exists, files currently in that directory will be overwritten. Continue?", None)
        if keepGoing:
            shutil.rmtree(nameOfDataSet + "_TEMP")
            shutil.rmtree(nameOfDataSet + "_Results")
            break
        else:
            nameOfDataSet = raw_input("Choose another name for the data set. ").lower().replace(" ", "")

#print(nameOfDataSet)

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
        while True:
            try:
                quadrant = int(raw_input("Which quadrant is this test in? "))
                if (quadrant >= 0 and quadrant <= 3):
                    break
                else:
                    print("That's an invalid quadrant number. Please pick a number in the range of [0-3].")
            except ValueError:
                print("Please type in a valid number")

	os.system("./multi.sh " + str(nameOfDataSet) + "_TEMP " + str(currentTestNumber) + " " + str(numberOfTrials))
        
        #Append quadrant information (expected output) to end of csv files
        currentTrialNumber = 1
        while (currentTrialNumber <= numberOfTrials):
            #fd = open("./" + str(nameOfDataSet) + "_TEMP/" + str(currentTestNumber) + "/" + str(currentTestNumber) + "_" + \
            #        str(currentTrialNumber) + "_GREPPED.csv", 'a')
            #if (quadrant == 0):
            #    myCSVRow = [1, 0, 0, 0]
            #    fd.write(myCSVRow)
            #elif (quadrant == 1):
            #    myCSVRow = [0, 1, 0, 0]
            #    fd.write(myCSVRow)
            #elif (quadrant == 2):
            #    myCSVRow = [0, 0, 1, 0]
            #    fd.write(myCSVRow)
            #elif (quadrant == 3):
            #    myCSVRow = [0, 0, 0, 1]
            #    fd.write(myCSVRow)
            #else: #quadrant # was already checked; this should never be called
            #    print("Error: Invalid quadrant")
            #fd.close()
            #currentTrialNumber += 1
            with open("./" + str(nameOfDataSet) + "_TEMP/" + str(currentTestNumber) + "/" + str(currentTestNumber) + "_" + \
                    str(currentTrialNumber) + "_GREPPED.csv", 'a') as file:
                writer = csv.writer(file)
                if (quadrant == 0):
                    myCSVRow = [1, 0, 0, 0]
                    writer.writerow(myCSVRow)
                elif (quadrant == 1):
                    myCSVRow = [0, 1, 0, 0]
                    writer.writerow(myCSVRow)
                elif (quadrant == 2):
                    myCSVRow = [0, 0, 1, 0]
                    writer.writerow(myCSVRow)
                elif (quadrant == 3):
                    myCSVRow = [0, 0, 0, 1]
                    writer.writerow(myCSVRow)
                else: #quadrant # was already checked; this should never be called
                    print("Error: Invalid quadrant")
            currentTrialNumber += 1

        print("Test number " + str(currentTestNumber) + " completed!  Now viewing trial 1 data:")
        try:
            os.system("cat ./" + str(nameOfDataSet) + "_TEMP/" + str(currentTestNumber) + "/" + str(currentTestNumber) + "_" + \
                "1_GREPPED.csv")
        except:
            if (numberOfTrials > 1):
                print("There was an error with trial #1. View a different trial?")  ##TO DO --> Ask yes or no
            else:
                print("There was an error with the test. Data wasn't properly collected.")
        
	#time.sleep(1)
	if (currentTestNumber == numberOfTests):
		choice = raw_input("Hit enter to process your completed tests, \"r\" to rerun the last test, [1-" + str(numberOfTrials) \
                        + "]\nto view that trial, or \"q\" to quit. ").lower()
	else:
		choice = raw_input("Move to the next position and hit enter when ready. To rerun the last test, type in \"r\".\n" \
                        + "To view the results of another trial, type in a number between [1-" + str(numberOfTrials) + "]: ").lower()
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
                elif (int(choice) >= 1 and int(choice) <= numberOfTrials):
                    try:
                        os.system("cat ./" + str(nameOfDataSet) + "_TEMP/" + str(currentTestNumber) + "/" + str(currentTestNumber) + "_" + \
                                str(choice) + "_GREPPED.csv")
                    except:
                        print("There was an error with that trial. Data wasn't properly collected.")
                    if (currentTestNumber == numberOfTests):
                        choice = raw_input("Hit enter to process completed tests, \"r\" to rerun the last test, or [1-" + str(numberOfTrials) \
                            + "]\nto view the data for that trial. ")
                    else:
                        choice = raw_input("Hit enter to begin the next test, \"r\" to rerun the last test, or [1-" + str(numberOfTrials) \
                                + "]\n to view the data for that trial. ")
		else:
			if (currentTestNumber == numberOfTests):
				choice = raw_input("Invalid Command. Please hit enter to process the completed tests, \"r\" to rerun the last test," \
                                        + "\n[1-" + str(numberOfTrials) + "] to view that trial, or \"q\" to quit. ").lower()
			else:
				choice = raw_input("Invalid Command. Please hit enter to begin testing, \"r\" to rerun the last test, " \
                                        + "\n[1-" + str(numberOfTrials) + "] to view that trial, or \"q\" to quit. ").lower()
print("All tests processed")

os.system("./movingScript.sh " + str(nameOfDataSet) + "_TEMP " + str(nameOfDataSet) + "_Results")
print("All tests moved to final processing folder.")
#if not (numberOfTests.isdigit()):
#	print("Not a digit")


