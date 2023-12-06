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
xml_prefix = r"\Sentinel_1_DeepSAR_"
# xml_prefix = r"Z:\SipamSAR\Scripts\SAR_Process"

DATA_FOLDER1 = homefolder + "\SLC1"
DATA_FOLDER2 = homefolder + "\SLC2"
DATA_FOLDER3 = homefolder + "\SLC3"
XML_FOLDER = homefolder + r"\Process_Chain"

Path("Results2").mkdir(exist_ok=True)
results = homefolder + r"\Results2"

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
        
get_count = 19
#%%

list_size = [12, 4, 4, 4, 2, 2, 2, 4, 2, 2, 4, 4, 4, 6, 6, 3, 3, 2, 14]
    
file_list = [None] * get_count

for i in range(get_count): 
    file_list[i] = [None] * list_size[i]


#%%

etapa = '0'
print('Iniciando Etapa ' + str(int(etapa)+1))
sulfix = "_etapa" + etapa
st = time.time()

out_path = results + "\etapa" + etapa
Path(out_path).mkdir(exist_ok=True)
checkfolder(out_path)
    
file_list[0][0] = DATA_FOLDER1 + str(process_all_slc(DATA_FOLDER1))
file_list[0][1] = DATA_FOLDER2 + str(process_all_slc(DATA_FOLDER2))
file_list[0][2] = DATA_FOLDER3 + str(process_all_slc(DATA_FOLDER3))
file_list[0][11] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_01" + ".dim")
file_list[0][3] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_02" + ".dim")
file_list[0][4] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_03" + ".dim")
file_list[0][5] = out_path + str(process_all_slc(DATA_FOLDER2)).replace('.zip', sulfix + "_01" + ".dim")
file_list[0][6] = out_path + str(process_all_slc(DATA_FOLDER2)).replace('.zip', sulfix + "_02" + ".dim")
file_list[0][7] = out_path + str(process_all_slc(DATA_FOLDER2)).replace('.zip', sulfix + "_03" + ".dim")
file_list[0][8] = out_path + str(process_all_slc(DATA_FOLDER3)).replace('.zip', sulfix + "_01" + ".dim")
file_list[0][9] = out_path + str(process_all_slc(DATA_FOLDER3)).replace('.zip', sulfix + "_02" + ".dim")
file_list[0][10] = out_path + str(process_all_slc(DATA_FOLDER3)).replace('.zip', sulfix + "_03" + ".dim")

xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

for xmlk in range(list_size[int(etapa)]):
    set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

out_path = results + "\etapa" + etapa
Path(out_path).mkdir(exist_ok=True)
checkfolder(out_path)

extc_xml(xml_folder, out_path)

# process_other2(xml_folder)

endt = time.time()

count_time(st, endt)
ttotal += st-endt
print('Fim da Etapa 1')

#  #%%

# etapa = '1'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa

# st = time.time()

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[1][0] = file_list[0][11]
# file_list[1][1] = file_list[0][5]
# file_list[1][2] = file_list[0][8]
# file_list[1][3] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_01" + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(4):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)

# endt = time.time()
# count_time(st, endt)
# print('Fim da Etapa 2')
# ttotal += st-endt
# #%%

# etapa = '2'
# st = time.time()
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[2][0] = file_list[0][3]
# file_list[2][1] = file_list[0][6]
# file_list[2][2] = file_list[0][9]
# file_list[2][3] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_02" + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(4):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)

# endt = time.time()
# count_time(st, endt)
# print('Fim da Etapa 3')
# ttotal += st-endt

# #%%

# etapa = '3'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa

# st = time.time()

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[0][4]
# file_list[int(etapa)][1] = file_list[0][7]
# file_list[int(etapa)][2] = file_list[0][10]
# file_list[int(etapa)][3] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_03" + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(4):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st, endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '4'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[1][3]
# file_list[int(etapa)][1] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_01" + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(2):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st, endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '5'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()


# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[2][3]
# file_list[int(etapa)][1] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_02" + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(2):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st, endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '6'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[3][3]
# file_list[int(etapa)][1] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_03" + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(2):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '7'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# xml_folder = XML_FOLDER + xml_prefix + etapa + "-1" + ".xml"
# extc_xml(xml_folder, out_path)

# file_list[int(etapa)][0] = file_list[4][1]
# file_list_aux1 = [None]* 2
# file_list_aux1[0] = file_list[int(etapa)][0]
# file_list_aux1[1] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "aux1" + ".dim")

# print("aux1")

# xml_folder = XML_FOLDER + xml_prefix + etapa + "-1" + ".xml"

# for xmlk in range(2):
#     set_xml_multi(xmlk, file_list_aux1[xmlk], xml_folder)
    
# process_other2(xml_folder)

# file_list[int(etapa)][1] = file_list[5][1]
# file_list_aux2 = [None]* 2
# file_list_aux2[0] = file_list[int(etapa)][1]
# file_list_aux2[1] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "aux2" + ".dim")

# print("aux2")

# xml_folder = XML_FOLDER + xml_prefix + etapa + "-2" + ".xml"

# for xmlk in range(2):
#     set_xml_multi(xmlk, file_list_aux2[xmlk], xml_folder)
    
# process_other2(xml_folder)

# file_list[int(etapa)][2] = file_list[6][1]
# file_list_aux3 = [None]* 2
# file_list_aux3[0] = file_list[int(etapa)][2]
# file_list_aux3[1] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "aux3" + ".dim")

# print("aux3")

# xml_folder = XML_FOLDER + xml_prefix + etapa + "-3" + ".xml"

# for xmlk in range(2):
#     set_xml_multi(xmlk, file_list_aux3[xmlk], xml_folder)
    
# process_other2(xml_folder)

# file_list[int(etapa)][3] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + ".dim")
# file_list_aux4 = [None]* 4
# file_list_aux4[0] = file_list_aux1[1]
# file_list_aux4[1] = file_list_aux2[1]
# file_list_aux4[2] = file_list_aux3[1]
# file_list_aux4[3] = file_list[int(etapa)][3]

# print("aux4")

# xml_folder = XML_FOLDER + xml_prefix + etapa + "-4" + ".xml"

# for xmlk in range(4):
#     set_xml_multi(xmlk, file_list_aux4[xmlk], xml_folder)
    
# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '8'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[7][3]
# file_list[int(etapa)][1] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(2):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '9'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[7][3]
# file_list[int(etapa)][1] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(2):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '10'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[0][11]
# file_list[int(etapa)][1] = file_list[0][3]
# file_list[int(etapa)][2] = file_list[0][4]
# file_list[int(etapa)][3] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(4):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '11'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[0][5]
# file_list[int(etapa)][1] = file_list[0][6]
# file_list[int(etapa)][2] = file_list[0][7]
# file_list[int(etapa)][3] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(4):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '12'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[0][8]
# file_list[int(etapa)][1] = file_list[0][9]
# file_list[int(etapa)][2] = file_list[0][10]
# file_list[int(etapa)][3] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(4):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '13'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[10][3]
# file_list[int(etapa)][1] = file_list[11][3]
# file_list[int(etapa)][2] = file_list[12][3]
# file_list[int(etapa)][3] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_02" +  ".dim")
# file_list[int(etapa)][4] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_03" + ".dim")
# file_list[int(etapa)][5] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_01" + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(6):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '14'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[8][1]
# file_list[int(etapa)][1] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_02" + ".dim")
# file_list[int(etapa)][2] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_03" + ".dim")
# file_list[int(etapa)][3] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_04" + ".dim")
# file_list[int(etapa)][4] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_05" + ".dim")
# file_list[int(etapa)][5] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + "_01" + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(6):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '15'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[14][5]
# file_list[int(etapa)][1] = file_list[14][1]
# file_list[int(etapa)][2] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(3):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '16'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[14][5]
# file_list[int(etapa)][1] = file_list[14][1]
# file_list[int(etapa)][2] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(3):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '17'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[8][1]
# file_list[int(etapa)][1] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(2):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('Fim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# #%%

# etapa = '18'
# print('Iniciando Etapa ' + str(int(etapa)+1))
# sulfix = "_etapa" + etapa
# st = time.time()
# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# file_list[int(etapa)][0] = file_list[8][1]
# file_list[int(etapa)][1] = file_list[9][1]
# file_list[int(etapa)][2] = file_list[13][5]
# file_list[int(etapa)][3] = file_list[13][3]
# file_list[int(etapa)][4] = file_list[13][4]
# file_list[int(etapa)][5] = file_list[14][5]
# file_list[int(etapa)][6] = file_list[14][1]
# file_list[int(etapa)][7] = file_list[14][2]
# file_list[int(etapa)][8] = file_list[14][3]
# file_list[int(etapa)][9] = file_list[14][4]
# file_list[int(etapa)][10] = file_list[15][2]
# file_list[int(etapa)][11] = file_list[16][2]
# file_list[int(etapa)][12] = file_list[17][1]
# file_list[int(etapa)][13] = out_path + str(process_all_slc(DATA_FOLDER1)).replace('.zip', sulfix + ".dim")

# xml_folder = XML_FOLDER + xml_prefix + etapa + ".xml"

# for xmlk in range(14):
#     set_xml_multi(xmlk, file_list[int(etapa)][xmlk], xml_folder)

# out_path = results + "\etapa" + etapa
# Path(out_path).mkdir(exist_ok=True)
# checkfolder(out_path)

# extc_xml(xml_folder, out_path)

# process_other2(xml_folder)
# endt = time.time()
# count_time(st,endt)
# print('\nFim da Etapa '+ str(int(etapa)+1))
# ttotal += st-endt
# count_time(ttotal, 0)

# with open('tempos.txt', 'a') as f:
#     f.write(f"\n {str(abs(ttotal))}")
# #%%





