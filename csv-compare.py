#!/usr/bin/env python3

import json
import os
import shutil
import argparse
from json2html import *
from csv_diff import load_csv, compare
from zipfile import ZipFile

BASEPATH = os.getcwd()

class CompareCSV():
    
    def __init__(self, firstFile, secondFile):
        self.firstZipFile = firstFile + '.zip'
        self.secondZipFile = secondFile + '.zip'
        self.firstFile = firstFile + '.csv'
        self.secondFile = secondFile + '.csv'
        self.jsonFile = BASEPATH + "\\data.json"
        self.templateHtml = BASEPATH + "\\compareOutputTemplate.html"
        self.outputHtml = BASEPATH + "\\compareOutput.html"

        self.compare_csv_files()
        
    def compare_csv_files(self):
        print("First File : %s \n Second File : %s" %(self.firstFile, self.secondFile))
        
        with ZipFile(self.firstZipFile, 'r') as f:
            f.extractall()
        with ZipFile(self.secondZipFile, 'r') as f:
            f.extractall()    
    
        if os.path.exists("compareOutput.html"):
            os.remove("compareOutput.html")
        
        diff = compare( load_csv(open(self.firstFile), key="Address"),
                        load_csv(open(self.secondFile), key="Address"))
        #print(diff)
        print("********* COMPARING CSV FILES AND COVERTING INTO JSON ********* ")

        # Converts input dictionary into json_string
        jsonString = json.dumps(diff)
        jsonFile = open(self.jsonFile, "w")
        jsonFile.write(jsonString)
        jsonFile.close()

        self.convert_json_html()

    def convert_json_html(self):
        print("********* COVERTING JSON INTO HTML ********* ")
        shutil.copy2(self.templateHtml, self.outputHtml)
        Func = open(self.outputHtml, "a")

        #adding heading to html file
        Func.write("<html>\n<head>\n<title> \nOutput Data in an HTML file\n \
               </title>\n <link rel='stylesheet' href='styles.css'>\n</head> <body> \n \
               <h2 color='#00b300'>File <span style='color:#0b8497;font-weight:bold'>{f1}</span> compared with File <span style='color:#0b8497;font-weight:bold'>{f2}</span>, as follows: </h2>\n</body></html>".format(f1="SBTS00_ENB_9999_220613_000011.csv", f2="SBTS00_ENB_9999_220613_000012.csv"))

        # Saving the data into the HTML file
        Func.close()

        #convert json to html
        with open(self.jsonFile) as csvJsonFile:
            csvJsonData = json.load(csvJsonFile)
            scanOutput = json2html.convert(json = csvJsonData)
            with open(self.outputHtml, 'a') as htmlfile: 
                htmlfile.write(str(scanOutput))
                print("********* Json file is converted into html successfully ********* ")

def get_args():
    pr = argparse.ArgumentParser()
    pr.add_argument('csvFile1', action='store', type=str)
    pr.add_argument('csvFile2', action='store', type=str)
    return pr.parse_args()


if __name__ == '__main__':

    print("********* AUTOMATED COMPARSION OF CSV FILES *********")

    #compare = CompareCSV(csvFile1=sys.argv[1], csvFile2=sys.argv[2])
    compare = CompareCSV(sys.argv[1], sys.argv[2])
    #compare = CompareCSV("SBTS00_ENB_9999_220613_000011", "SBTS00_ENB_9999_220613_000012")
    
        
