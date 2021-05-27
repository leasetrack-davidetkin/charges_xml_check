# LeaseTrack
# Charges Check Report Generator

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

cols = ["Filename", "Charges", "Errors"]
output = []
tcodes = []
def read_xml(xml, comment, TransactionDate, ServiceToDate, ChargeCode):
    file_output = []
    tree = ET.parse(xml)
    root = tree.getroot()
    count = 0
    errors = 0
    for child in root:
        for detail in child:
            count = int(detail.attrib["Count"])
    return [count, errors]

def check(input_dir, output_dir, output_name, comment, TransactionDate, ServiceToDate, ChargeCode):
    filecount = 0
    total_count = 0
    total_errors = 0
    output = []
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

    filename = output_dir + output_name
    pd.DataFrame(output, columns=cols).to_csv(filename, index=None)

directory = r'C:\Users\ALB006\Documents\Charges XML Check\brookfield-in'
comment = "Tenant Legal Liability (05/2021)"
date = "2021-05-01"
output_name = "/output.csv"
output_dir = "brookfield-out"
charge_code = "200092"

check(directory, output_dir, output_name, comment, date, date, charge_code)

def checkIfDuplicates_3(listOfElems):
    duplicate_count  = 0
    for elem in listOfElems:
        if listOfElems.count(elem) > 1:
            duplicate_count += 1
            print("duplicate", elem)
    print(duplicate_count, "duplicates")

#checkIfDuplicates_3(tcodes)