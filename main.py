# Housing Project
# Final Project for BDS-754 Principles of Programming with Python
# Neil Maneck
# Fall 2020

from files import *
import functions
import pymysql
import creds

print("Beginning import")


# Loader function drops corrupt guid but does not check for additional corrupt data.
# See functions.py
print("Cleaning Housing File data")
loadHouse = functions.loader(housingFile)
houseRecs = len(loadHouse)
print(f"{houseRecs} records imported into the database")

print("Cleaning Income File data")
loadIncome = functions.loader(incomeFile)
incomeRecs = len(loadIncome)
print(f"{incomeRecs} records imported into the database")

print("Cleaning ZIP File data")
loadZip = functions.loader(zipFile)
zipRecs = len(loadZip)
print(f"{zipRecs} records imported into the database")

# Create dictionary with shallow merge of three dictionaries by guid.
# Note shallow merge overwrites guids and zip-codes of previous entries.
mergeDict = dict()
for guid in loadHouse:
    mergeDict[guid] = {**loadHouse[guid], **loadZip[guid], **loadIncome[guid]}

# Cleaner function to remove all non-guid corrupt data.
# See functions.py
functions.cleaner(mergeDict)

# Opens pymysql connection.
# See creds.py to set credentials
myConnection = pymysql.connect(host=creds.host,
                               user=creds.user,
                               password=creds.password,
                               db="housing_project",
                               charset='utf8mb4',
                               cursorclass=pymysql.cursors.DictCursor)


# Creates an insert command for each guid and then executes the command.
# Order of keys in each dictionary was determined manually (code since deleted)
for guid in mergeDict:
    editCommand = "INSERT INTO housing (guid, zip_code, median_age, total_rooms, total_bedrooms, population, households, " \
                  "median_house_value, city, state, county, median_income) VALUES ('"
    editCommand += guid
    for key in mergeDict[guid]:
        editCommand += "','" + mergeDict[guid][key]
    editCommand += "');"
    with myConnection.cursor() as cursor:
        cursor.execute(editCommand)
    myConnection.commit()

print("Import completed")

print()
print("Beginning validation")
print()

rooms = input("Total Rooms:")

roomSql = """select
    sum(total_rooms)
    from
    housing
    where
    total_rooms > %s
"""

# Sends provided roomSql command to get total rooms
with myConnection.cursor() as cursor:
    cursor.execute(roomSql, rooms)
    output = cursor.fetchall()
myConnection.commit()

# Need to extract total rooms from dictionary inside of list format provided by pymysql DictCursor.
totalRooms = output[0]['sum(total_rooms)']
print(f"For locations with more than {rooms} rooms, there are a total of {totalRooms} ")

print()
zip_code = input("ZIP Code:")

incomeSql = """select
    format(round(avg(median_income)),0)
    from
    housing
    where
    zip_code = %s
"""

# Sends incomeSql command to SQL
with myConnection.cursor() as cursor:
    cursor.execute(incomeSql, zip_code)
    output = cursor.fetchall()

myConnection.commit()

# Need to extract median_income from dictionary inside of list format.
median_income = output[0]['format(round(avg(median_income)),0)']

print(f"The median household income for ZIP code {zip_code} is {median_income}.")
print()
print("Program exiting.")
