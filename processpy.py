# -*- coding: utf-8 -*-
"""
Created on Tue Nov 28 16:18:23 2023

@author: ciro.rocha
"""
import os
import sys
import subprocess
import xml.etree.ElementTree as ET
import os
import sys
from pathlib import Path
import warnings
import time

from glob import glob


SAVE_FILE = "results"
GPT_FOLDER = r"C:\Program Files\snap\bin\gpt.exe" 



if not os.path.exists(GPT_FOLDER):
    print("GPT not found in {}".format(GPT_FOLDER))
    print("Change GPT_FOLDER variable in process.py")
    sys.exit(1)

def process_all_slc(DATA_FOLDER):
  
    if not os.path.exists(DATA_FOLDER):
        print("Data folder not found in {}".format(DATA_FOLDER))
        print("Change data_path variable in main.py")
        sys.exit(1)


    slc_paths = glob(os.path.join(DATA_FOLDER, '**', '*.zip'), recursive=True)
    file = str(slc_paths)
    size_file = len(file)
    s1a_find = file.find('S1A') - 1
    file_name =file[s1a_find:size_file - 2]

    return(file_name)

        
# def process_other(slc_path, out_name, xml_chain):
#     try:
#         result = subprocess.run([GPT_FOLDER, xml_chain], capture_output=True, text=True)
#     except subprocess.CalledProcessError as e:
#         print("Error: ", e)
#         return
#     if result.returncode != 0:
#         print("Error: ", result.stderr)
#         return
    
def process_other2(xml_chain):
#mesma funcao do process_other porem utilizando como entrada apenas a localizacao do xml
    try:
        result = subprocess.run([GPT_FOLDER, xml_chain], capture_output=True, text=True)
    except subprocess.CalledProcessError as e:
        print("Error: ", e)
        return
    if result.returncode != 0:
        print("Error: ", result.stderr)
        return
    
def set_xml(pathin, pathout, filexml):
    
    mytree = ET.parse(filexml)
    myroot = mytree.getroot()

    setinandout = "in"
    for files in myroot.iter('file'):
        
        if setinandout == "in":
            files.text = pathin
            mytree.write(filexml)
        else:
            files.text = pathout
            mytree.write(filexml)
            
        setinandout = "out"
        
def set_xml_multi(xmlk, file_list, xml_folder):
    
    i = 0
    k = xmlk
    
    mytree = ET.parse(xml_folder)
    myroot = mytree.getroot()

    for files in myroot.iter('file'):
        if k == i:
            files.text = file_list
            mytree.write(xml_folder)
        
        i = i + 1
        
def extc_xml(filexml, output_path):
    
    mytree = ET.parse(filexml)
    myroot = mytree.getroot()

    file_name = output_path + "\PROCESS STEPS.txt"
    
    with open(file_name, "w") as file:
        file.write("Processamento aplicado nessa etapa:" + os.linesep)
    
    for operations in myroot.iter('operator'):
        
        if not operations.text == 'Read':
            if not operations.text == 'Write':
                
                with open(file_name, "a") as file:
                    file.write(operations.text + os.linesep)

        
def set_output(input_file, out_path, sulfix):
    
    s1a_find = input_file.find('S1A')
    size_file = len(input_file)
    file_name = input_file[s1a_find:size_file - 4]
    outfile = file_name + sulfix
    outresult = out_path + '\\' + outfile
    
    return outresult
        
        
def checkfolder (FOLDER):
    
    if not os.path.exists(FOLDER):
        print("Data" + FOLDER + "not found in {}".format(FOLDER))
        print("Check the path of the " + FOLDER + " and make sure it exists")
        sys.exit(1)
    
def count_steps (xml_path):
    xml_count = 0
    for path in os.listdir(xml_path):
        if os.path.isfile(os.path.join(xml_path, path)):
            xml_count += 1
    print('Numero de etapas:', xml_count)
    return xml_count

def count_time(st, endt):
    if endt - st < 60:
        print(f"time elapsed: {(endt - st):.2f} segundos")
    elif 60 <= (endt - st) <= 3600:
        minutes = (endt - st) // 60
        seconds = (endt - st) % 60
        print(f"time elapsed: {minutes:.0f} minuto(s) e {seconds:.2f} segundos")
    else:
        hours = (endt - st) // 3600
        remaining_minutes = ((endt - st) % 3600) // 60
        seconds = (endt - st) % 60
        print(f"time elapsed: {hours:.0f} hora(s), {remaining_minutes:.0f} minutos, and {seconds:.2f} segundos")
ttotal = 0


#%%

warnings.filterwarnings("ignore", category=UserWarning) 

if __name__ == "__main__":

    homefolder = os.getcwd()

#%%   
xml_prefix = r"\SAR_Processing_Chain_Blue_Amazon_"
# xml_prefix = r"Z:\SipamSAR\Scripts\SAR_Process"

DATA_FOLDER1 = homefolder + "\SLC1"
DATA_FOLDER2 = homefolder + "\SLC2"
XML_FOLDER = homefolder + r"\Process_Chain"

Path("Results2").mkdir(exist_ok=True)
results = homefolder + r"\Results"

checkfolder(homefolder)
checkfolder(XML_FOLDER)
checkfolder(results)

print("Valor e de:", XML_FOLDER)
#%%

get_count = 0
get_file = [None] * count_steps(XML_FOLDER)

for file in os.listdir(XML_FOLDER):
    if file.endswith(".xml"):
        file_path = f"{XML_FOLDER}\{file}"
        get_file[get_count] = file_path
        get_count = get_count + 1

        
#%%

list_size = [12, 4, 4, 4, 2, 2, 2, 4, 2, 2, 4, 4, 4, 6, 6, 3, 3, 2, 14]
    
file_list = [None] * get_count

for i in range(get_count): 
    file_list[i] = [None] * list_size[i]

