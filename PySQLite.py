import sqlite3
import os
import sys
import csv

"""
Script to automate common SQLite queries in Digital Forensic Database
- Audit
    - Check for unassigned cases
    - Check where evidence is stored for a particular case
    - Audit cases on am evidence drive
    - List number of cases by year/a`ll
    - List cases by investigator by year/all
    - List open cases by investigator
    - Check disposition status of evidence (evidence #, contains CP)
    - Count/List ICAC cases by year/all

- Entry
    - Enter New Forensic Case
    - Update a case
    - Assign Forensic Investigator
    - Add Evidence (type, status, location)
    - Completed (date)
    
"""

__author__ = "Darrin Schultz"
__version__ = "1.0.0"
__date__ = "2018-12-30"
__copyrite__ = "Copyrite 2018, Eagan Police Department"
__email__ = "dschultz@cityofeagan.com"


# Check for all assigned cases
def unassignedCases():
    try:
        result = theCursor.execute("SELECT case_num, date_requested, case_desc FROM cases WHERE forensic_inv IS 'NULL'")
        print("UNASSIGNED FORENSIC CASES: \n")
        x = "CASE NUMBER"
        y = "DATE REQUESTED"
        z = "DESCRIPTION"
        print('{:15}{:17}{:<20}'.format(x,y,z))
        print('-'*43)
        for row in result:
            print("{:<15}{:<17}{:<20}".format(row[0],row[1],row[2]))
    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    except:
        print("Couldn't Retrieve Data from Database")


# Check where evidence is stored for a particular case.
def drives_by_case(cn):
    case = cn
    try:
        result =  theCursor.execute("SELECT drive_num, case_num, forensic_inv FROM cases, evidence_drives WHERE cases.case_num = evidence_drives.case_id AND case_id LIKE ('{}')".format(case))
        print("Drives Containing Forensic Evidence by Case ('{}'): \n".format(case))
        x = "DRIVE NUMBER"
        y = "CASE NUMBER"
        z = "INVESTIGATOR"
        print('{:15}{:15}{:15}'.format(x,y,z))
        print('-'*43)
        for row in result:
            print("{:^15}{:<15}{:^12}".format(row[0],row[1],row[2]))
    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    except:
        print("Couldn't Retrieve Data from Database")

# Audit cases on Evidence Drive
def cases_on_drive(dn):
    drive = dn
    try:
        result = theCursor.execute("SELECT case_num, forensic_inv, drive_num FROM cases, evidence_drives WHERE cases.case_num = evidence_drives.case_id AND drive_num = ('{}')".format(drive))
        print("Cases on drive '{}' are: \n".format(drive))
        x = "CASE NUMBER"
        y = "INVESTIGATOR"
        z = "DRIVE NUMBER"
        print("{:15}{:19}{:15}".format(x,y,z))
        print('-'*46)
        for row in result:
            print("{:<15}{:<19}{:^15}".format(row[0],row[1],row[2]))
    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    except:
        print("Couldn't Retrieve Data from Database")


# List all cases or cases by year/all
def caseYear(cy):
    year = cy
    try:
        if year.isdigit():
            result = theCursor.execute("SELECT case_num, date_requested, date_completed, forensic_inv FROM cases WHERE date_requested LIKE ('%{}%')".format(year))
            print("\nCases in '{}' are: \n".format(year))
            w = "CASE NUMBER"
            x = "REQUESTED"
            y = "COMPLETED"
            z = "INVESTIGATOR"
            print('{:15}{:15}{:15}{:15}'.format(w,x,y,z))
            print('-'*61)
            for row in result:
                print("{:^15}{:<15}{:<15}{:<15}".format(row[0],row[1],row[2],row[3]))
        elif year.lower() != 'a':
            print("You must enter a year or 'a' for all. ")
        elif year.lower() == 'a':
            result = theCursor.execute("SELECT case_num, date_requested, date_completed, forensic_inv FROM cases")
            print("\nCases in '{}' are: \n".format(year))
            w = "CASE NUMBER"
            x = "REQUESTED"
            y = "COMPLETED"
            z = "INVESTIGATOR"
            print('{:15}{:15}{:15}{:15}'.format(w,x,y,z))
            print('-'*61)
            for row in result:
                print("{:^15}{:<15}{:<15}{:<15}".format(row[0],row[1],row[2],row[3]))


    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    except:
        print("Couldn't Retrieve Data from Database")

#List cases processed by year/all
def invCaseYear(ic, y):
    inv = ic
    year = y
    try:
        if year.isdigit():
            result = theCursor.execute("SELECT case_num, date_requested, date_completed, forensic_inv FROM cases WHERE date_requested LIKE ('%{}%') and forensic_inv LIKE ('%{}%')".format(year, inv))
            print("\nCases in '{}' by '{}' are: \n".format(year,inv))
            w = "CASE NUMBER"
            x = "REQUESTED"
            y = "COMPLETED"
            z = "INVESTIGATOR"
            print('{:15}{:15}{:15}{:15}'.format(w,x,y,z))
            print('-'*61)
            for row in result:
                print("{:^15}{:<15}{:<15}{:<15}".format(row[0],row[1],row[2],row[3]))
        elif year.lower() != 'a':
            print("You must enter a year or 'a' for all. ")
        elif year.lower() == 'a':
            result = theCursor.execute("SELECT case_num, date_requested, date_completed, forensic_inv FROM cases WHERE forensic_inv LIKE ('%{}%')".format(inv))
            print("\nCases by '{}' are: \n".format(inv))
            w = "CASE NUMBER"
            x = "REQUESTED"
            y = "COMPLETED"
            z = "INVESTIGATOR"
            print('{:15}{:15}{:15}{:15}'.format(w,x,y,z))
            print('-'*61)
            for row in result:
                print("{:^15}{:<15}{:<15}{:<15}".format(row[0],row[1],row[2],row[3]))

    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    except:
        print("Couldn't Retrieve Data from Database")


#List open cases by investigator
def openInv(inv):
    i = inv
    try:
        result = theCursor.execute("SELECT case_num, forensic_inv, date_requested, date_completed FROM cases WHERE date_completed IS 'NULL' and forensic_inv IS ('{}')".format(i))
        print("\nOpen cases by {}:  \n".format(i))
        w = "CASE NUMBER"
        x = "INVESTIGATOR"
        y = "REQUEST DATE"
        z = "DESCRIPTION"
        print('{:15}{:15}{:15}{:9}'.format(w,x,y,z))
        print('-'*58)
        for row in result:
            print("{:^15}{:<15}{:<15}{:<9}".format(row[0],row[1],row[2],row[3]))
    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    except:
        print("Couldn't Retrieve Data from Database")


#Check disposition status of evidence (has evidence, contains CP)
def dispo(case):
    c = case
    try:
        result = theCursor.execute("SELECT case_num, case_desc, evid_num, has_cp FROM cases, evidence_status WHERE cases.case_num = evidence_status.case_id AND case_num IS '{}'".format(c))
        print("\nEvidence dispo status for '{}': \n".format(c))
        t = "CASE NUMBER"
        u = "DESCRIPTION"
        v = "EVIDENCE #"
        w = "HAS CP"
        print("{:13}{:29}{:12}{:10}".format(t,u,v,w))
        print("-"*100)
        for row in result:
            print("{:<13}{:<29}{:^10}{:^10}".format(row[0],row[1],row[2],row[3]))
    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    except:
        print("Couldn't Retrieve Data from Database")


#List ICAC cases by year/all
def icac(year):
    y = year
    try:
        if str(y).isdigit():
            result = theCursor.execute("SELECT case_num, date_requested, date_completed, forensic_inv, icac_dispo, is_icac FROM cases WHERE is_icac IS 1 AND date_requested LIKE ('%{}%')".format(year))
            print("\nICAC cases in '{}' are: \n".format(year))
            v = "CASE NUMBER"
            w = "REQUESTED"
            x = "COMPLETED"
            y = "INVESTIGATOR"
            z = "ICAC DISPO"
            print('{:15}{:13}{:13}{:25}{:15}'.format(v,w,x,y,z))
            print('-'*76)
            for row in result:
                print("{:<15}{:<13}{:<13}{:<25}{:^10}".format(row[0],row[1],row[2],row[3],row[4]))
        elif year.lower() != 'a':
            print("You must enter a year or 'a' for all. ")
        elif year.lower() == 'a':
            result = theCursor.execute("SELECT case_num, date_requested, date_completed, forensic_inv, icac_dispo, is_icac FROM cases WHERE is_icac IS 1")
            print("\nICAC cases \n")
            v = "CASE NUMBER"
            w = "REQUESTED"
            x = "COMPLETED"
            y = "INVESTIGATOR"
            z = "ICAC DISPO"
            print('{:15}{:13}{:13}{:25}{:15}'.format(v,w,x,y,z))
            print('-'*76)
            for row in result:
                print("{:<15}{:<13}{:<13}{:<25}{:^10}".format(row[0],row[1],row[2],row[3],row[4]))
    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    except:
        print("Couldn't Retrieve Data from Database")

# This section is for database entry and update

#    - Enter New Forensic Case
#       - case_number (8 digit without dash)
#       - case_desc (Short Case Desc)
#       - forensic_only (y or n)
#       - is_icac (y or n)
#       - icac_dispo (ICAC Data System Updated y or n)
#       = date requested (Format 2019-01-01)
#       = date completed (Format 2019-0101)
#       - Reporting Officer
#       - Forensic Investigator if assigned)


def entCase():
    y = year
    try:
        if str(y).isdigit():
            result = theCursor.execute("SELECT case_num, date_requested, date_completed, forensic_inv, icac_dispo, is_icac FROM cases WHERE is_icac IS 1 AND date_requested LIKE ('%{}%')".format(year))
            print("\nICAC cases in '{}' are: \n".format(year))
            v = "CASE NUMBER"
            w = "REQUESTED"
            x = "COMPLETED"
            y = "INVESTIGATOR"
            z = "ICAC DISPO"
            print('{:15}{:13}{:13}{:25}{:15}'.format(v,w,x,y,z))
            print('-'*76)
            for row in result:
                print("{:<15}{:<13}{:<13}{:<25}{:^10}".format(row[0],row[1],row[2],row[3],row[4]))
        elif year.lower() != 'a':
            print("You must enter a year or 'a' for all. ")
        elif year.lower() == 'a':
            result = theCursor.execute("SELECT case_num, date_requested, date_completed, forensic_inv, icac_dispo, is_icac FROM cases WHERE is_icac IS 1")
            print("\nICAC cases \n")
            v = "CASE NUMBER"
            w = "REQUESTED"
            x = "COMPLETED"
            y = "INVESTIGATOR"
            z = "ICAC DISPO"
            print('{:15}{:13}{:13}{:25}{:15}'.format(v,w,x,y,z))
            print('-'*76)
            for row in result:
                print("{:<15}{:<13}{:<13}{:<25}{:^10}".format(row[0],row[1],row[2],row[3],row[4]))
    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    except:
        print("Couldn't Retrieve Data from Database")



#    - Update a case
#    - Assign Forensic Investigator
#    - Add Evidence (type, status, location)
#    - Completed (date)






#    - Enter New Forensic Case

def getOfc(x):
    name = x
    try:
        result = theCursor.execute("SELECT officer_name FROM officer WHERE officer_name IS ('{}')".format(name))
        for row in result:
            if row[0].isalnum():
                return row[0]
    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    return 'Null'

def getFofc(x):
    name = x
    try:
        result = theCursor.execute("SELECT officer_name FROM officer WHERE officer_name IS ('{}')".format(name))
        for row in result:
            if row[0].isalnum():
                return row[0]

    except sqlite3.OperationalError:
        print("The Table Doesn't Exist")
    return 'Null'


class Case:
    """Creates elements of a new forensic case and verifies they are in the correct format
    to be inserted into the database. """

    def __init__(self, c_num):
        self.c_num = c_num
        while True:
            try:
                if '-' in self.c_num:
                    raise ValueError
                elif self.c_num.strip() == "":
                    raise ValueError
                elif self.c_num.isalpha():
                    raise ValueError
                elif len(self.c_num) > 8:
                    raise ValueError
                elif len(self.c_num) < 8:
                    raise ValueError
                else:
                    self.c_num = int(self.c_num)
                    break
            except ValueError:
                print("You must enter an 8 digit number exactly without a dash. \n")

    def c_desc(self):
        ''''Checks if user inputs a description < 31 characters.'''
        while True:
            desc = input("\nEnter a brief case description:  \n")
            try:
                if desc.split() == "":
                    raise ValueError
                elif len(desc) > 31:
                    raise ValueError
                else:
                    return desc
            except ValueError:
                print("This field is required and must be limited to 30 characters.  \n")

    def rp_ofc(self):
        """Calls getOfc() function to check if user input is in the database.
            if the name is not in the database nothing will return."""
        while True:
            ofc = input("\nEnter the reporting officer's name: \n")
            try:
                if ofc.strip() == "":
                    raise ValueError
                else:
                    x = getOfc(ofc)
                    if x == 'Null':
                        raise ValueError
                    return x
            except ValueError:
                print("This field is required.  Enter a valid reporting officer's name \n")

    def f_inv(self):
        """Calls getOfc() function to check if user input is in the database.
            if the name is not in the database nothing will return."""
        while True:
            ofc = input("\nEnter the assigned forensic investigator or return if not assigned:  \n")
            try:
                if ofc.strip() == "":
                    break
                else:
                    x = getFofc(ofc)
                    if x == 'Null':
                        raise ValueError
                    return x
            except ValueError:
                print("Invalid Name.  Try again or 'enter' if no investigator assigned:  \n")


    def f_only(self):
        """Requires 'y' or 'n' answer.  Returns boolean 0 or 1."""
        while True:
            fnnx = input("\nIs this case 'Forensic Only'? 'y' or 'n':  \n")
            try:
                if fnnx == "":
                    raise ValueError
                elif fnnx != 'y' and fnnx != 'n':
                    raise ValueError
                else:
                    if fnnx.lower() == 'y':
                        return 1
                    if fnnx.lower() == 'n':
                        return 0
            except ValueError:
                print("\nThis is a required field. 'y' for yes and 'n' for no.  \n")


    def is_icac(self):
        """Requires 'y' or 'n' answer.  Returns boolean 0 or 1."""
        while True:
            icac = input("\nIs this an ICAC case? 'y' or 'n':  \n")
            try:
                if icac == "":
                    raise ValueError
                elif icac != 'y' and icac != 'n':
                    raise ValueError
                else:
                    if icac.lower() == 'y':
                        return 1
                    if icac.lower() == 'n':
                        return 0
            except ValueError:
                print("\nThis is a required field. 'y' for yes and 'n' for no.  \n")




os.chdir("/Users/ComputerForensicUnit/Documents/Pycharm/ForensicDB")
db_conn = sqlite3.connect('caseTrackerV1.db')
print("CONNECTED TO THE DATABASE \n")


theCursor = db_conn.cursor()



#unassignedCases()
#drives_by_case(18000726)
#cases_on_drive(45)
#caseYear("2018")
#invCaseYear('Schultz', "2018")
#openInv('Schultz')
#dispo(18006495)
#icac(2018)


#newCase = Case("19009999")
#print(newCase.c_num)
#print(newCase.c_desc())
#print(newCase.rp_ofc())
#print(newCase.f_inv())
#print(newCase.f_only())
#print(newCase.is_icac())



with open('dump.sql', 'w') as f:
    for line in db_conn.iterdump():
        f.write(line)

db_conn.close()

print("\n"*3)
print("Database Closed")

