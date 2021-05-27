############################################
###              LeaseTrack              ###
###       Monthly Export Check Tool      ###
############################################

#region Imports
import csv
import pandas as pd
from scipy import stats
import numpy as np
import math
import datetime
import json
import re
import xml.etree.ElementTree as ET
import os
from pathlib import Path
#endregion

def print_msg_box(msg, indent=1, width=None, title=None):
    """Print message-box with optional title."""
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)

#region init
cols = ["Filename", "Charges", "Errors"]
output = []
tcodes = []
#endregion

def read_xml(xml, comment, TransactionDate, ServiceToDate, ChargeCode):
    file_output = []
    tree = ET.parse(xml)
    root = tree.getroot()
    count = 0
    errors = 0
    unitId = ""
    for child in root.findall("charges"):
        for detail in child:
            if(bool(re.search("UnitID", detail.tag))):
                unitId = detail.text
            if(bool(re.search("Comment", detail.tag))):
                text = detail.text
                if(text != comment):
                    errors += 1
                    print("ERROR: COMMENT MISMATCH for unit id:", unitId) 
            if(bool(re.search("TransactionDate", detail.tag))):
                text = detail.text
                if(text != TransactionDate):
                    errors += 1
                    print("ERROR: TransactionDate MISMATCH for unit id:", unitId) 
            if(bool(re.search("ServiceToDate", detail.tag))):
                text = detail.text
                if(text != ServiceToDate):
                    errors += 1
                    print("ERROR: ServiceToDate MISMATCH for unit id:", unitId) 
            if(bool(re.search("ChargeCode", detail.tag))):
                text = detail.text
                if(text != ChargeCode):
                    errors += 1
                    print("ERROR: ChargeCode MISMATCH for unit id:", unitId) 
            if(bool(re.search("CustomerID", detail.tag))):
                text = detail.text
                tcodes.append(text)
        count += 1
    return [count, errors]
    
def checkIfDuplicates(listOfElems):
    duplicate_count  = 0
    for elem in listOfElems:
        if listOfElems.count(elem) > 1:
            duplicate_count += 1
            print("duplicate", elem)
    return duplicate_count

def check(input_dir, output_dir, output_name, comment, TransactionDate, ServiceToDate, ChargeCode):
    filecount = 0
    total_count = 0
    total_errors = 0
    output = []
    print_msg_box("BEGIN SCAN")
    for file in os.listdir(input_dir):
        line = []
        data_folder = Path(os.path.basename(os.path.normpath(input_dir)))
        xml = data_folder / file
        print("----------------------")
        print("Begin scan for: ", file)
        r = read_xml(xml, comment, TransactionDate, ServiceToDate, ChargeCode)
        c = r[0]
        e = r[1]
        total_count += c
        total_errors += e
        line.append(file)
        line.append(c)
        line.append(e)
        print("CHARGES:", c)
        print("ERRORS:", e)
        output.append(line)
        filecount += 1
    print(filecount, "Files scanned")
    print("----------------------")

    output.append(["Total", total_count, total_errors])
    total_charges = total_count
    filename = output_dir + output_name
    pd.DataFrame(output, columns=cols).to_csv(filename, index=None)
    duplicates = checkIfDuplicates(tcodes)
    return [total_count, total_errors, filecount, duplicates]

#region########### USER INPUT VALUES ##################
property_name = "kff"
comment = "Insurance Exemption (06/2021)"
charge_code = "optoutfe"
date = "2021-06-01"
#endregion#############################################

#region Directory
directory = r"C:\Users\ALB006\Documents\Charges XML Check\\" + property_name + "-in"
output_name = "/output.csv"
output_dir = property_name + "-out"
#endregion

result = check(directory, output_dir, output_name, comment, date, date, charge_code)

#region Print result
print("Output to:", output_dir+".csv")
result_string = str(result[0]) + " charges, " \
    + str(result[2]) + " communities, " \
    + str(result[1]) + " errors, " \
    + str(result[3]) + " duplicates"
print_msg_box(result_string, indent=2, title="Result")
#endregion
