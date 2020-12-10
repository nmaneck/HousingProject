import csv
import re
import random

# Regex pattern for corrupt data.
corruptPattern = re.compile(r"^[A-Z]{4}$")


# Function to load csv into dictionary format keyed by guid. See comment below for more format information.
# Note: function works on all three files.
def loader(file):
    #Empty dictionary to store output
    outDict = dict()

    with open(file, newline='') as csvfile:
        reader = csv.reader(csvfile)
        #Grabs first line of csv file and saves it as a list of labels
        labels = next(reader)
        for row in reader:
            guid = row[0]
            # Makes sure that guid is not corrupt before adding it to dictionary
            if not corruptPattern.match(guid):
                # For each guid, creates a dictionary entry with the following format:
                # guid: {"first label":"first entry",
                #         "second label":"second entry,
                #         ...
                #         }
                outDict[guid] = {
                    labels[i]: row[i] for i in range(1,len(labels))
                }

    return outDict

# Cleaner detects whether or not data matches corrupt pattern. If the data is corrupt, passes off key and state to
# uncorrupter function. See below.
def cleaner(inDict):
    for guid in inDict:
        for key in inDict[guid]:
            if corruptPattern.match(inDict[guid][key]):
                # Note that integers are converted to strings so that data is consistent.
                inDict[guid][key] = str(uncorrupter(key, inDict[guid]['state']))

# Uncorrupter function replaces corrupt data based on specifications. State is necessary for replacing zip code
def uncorrupter(key, state):
    if key == 'housing_median_age':
        return random.randint(10, 50)
    elif key == 'total_rooms':
        return random.randint(1000, 2000)
    elif key == 'total_bedrooms':
        return random.randint(1000, 2000)
    elif key == 'population':
        return random.randint(5000, 10000)
    elif key == 'households':
        return random.randint(500, 2500)
    elif key == 'median_house_value':
        return random.randint(100000, 250000)
    elif key == 'median_income':
        return random.randint(100000, 750000)
    elif key == 'zip_code':
        if state == 'TX':
            return 70000
        elif state == ('NM' or 'AZ'):
            return 80000
        elif state == 'CA':
            return 90000
        else:
            print(f"ERROR: Unexpected state {entry['state']}")
    else:
        print(f"ERROR: Unexpected key {key}")
