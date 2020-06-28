#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  3 12:55:45 2020

@author: eric
"""
import os, sys, glob, random, csv, subprocess, datetime, time, re
from importlib import reload


dcmtk=input("Please enter the drive and root path where the DCMTK tools can be located:\n")

foundit2=""
foundit3=""

for root, dirs, files in os.walk(dcmtk):
    for file in files:
       if file.startswith('dcmodify'):
             foundit2 = True
             dcmtk_loc=(os.path.join(root, file))
             print(dcmtk_loc)
       if file.startswith('dcmdump'):
             dcmdump_loc=(os.path.join(root, file))
             foundit3 = True
             print(dcmdump_loc)
    if foundit2==True and foundit3 == True: break
else:
    dcmtk_loc="" #This inelegant solution does the following: setting a value to loc in the event that no DICOM files are found - otherwise no value would be set in loc which would break the approach to create loc_split
    print("set to null")

if dcmtk_loc != "": # If we find that loc has a value then we take the next step - splitting the loc destimation to get the path that we can use later in the code
   dcmtk_loc_split=os.path.dirname(dcmtk_loc)
   print(dcmtk_loc_split)
   print("DCMTK tools have been located, moving on")
  #print(dcmtk_loc_split)
else:
    print("No DCMTK tools were found - exiting")
    sys.exit(5)

os.chdir(dcmtk_loc_split)




dcm4che=input("Please enter the drive and root path where the DCM4CHE tools can be located:\n")

#dicom4che=dirpath.split(os.path.sep)[-1]
foundit4=""

for root, dirs, files in os.walk(dcm4che):
    for file in files:
         if file.startswith('dcm2dcm'):
            foundit4 = True
            dcm4che_loc=(os.path.join(root, file))
            print(dcm4che_loc)
            print(foundit4)
    if foundit4 == True: break     

else:
    dcm4che_loc="" #This inelegant solution does the following: setting a value to loc in the event that no DICOM files are found - otherwise no value would be set in loc which would break the approach to create loc_split
    print("set to null")
    print(dcmdump_loc)
if dcm4che_loc != "": # If we find that loc has a value then we take the next step - splitting the loc destimation to get the path that we can use later in the code
   dcm4che_loc_split=os.path.dirname(dcm4che_loc)
   print(dcm4che_loc_split)
   print("DCM4CHE tools have been located, moving on")
  #print(dcmtk_loc_split)
else:
    print("No DC4MCHE tools were found - exiting")
    sys.exit(5)


#----------------------------This code is for dumping dicom data via the dicom dump utility - save for later for an update.--------------
#for i in range(len(dcm_path_uq)):
    #dump_path_dbm = (dcm_path_uq[i])
    #print(dump_path_dbm)
    #imagedata_dbm.append(subprocess.run([dcmdump_loc, "+P", "0008,0060", "+sd", dump_path_dbm], stdout=subprocess.PIPE).stdout.decode('utf-8'))

#print(imagedata_dbm)


#------------------------------Below is the original part of the program which looks for files locally----------------------------------------------------


#r=datetime.datetime.now()


#for file in files:
    #if file.endswith((".dco", ".dcm")):
            #foundit = True
            #loc=(os.path.join(root, file))
            #print(loc)
    #if foundit==True: break
#else: 
    #loc="" #This inelegant solution does the following: setting a value to loc in the event that no DICOM files are found - otherwise no value would be set in loc which would break the approach to create loc_split
    #print("set to null")
            
#if loc != "": #If we find that loc has a value then we take the next step - splitting the loc destimation to get the path that we can use later in the code
   #loc_split=os.path.dirname(loc)
   #print(loc_split)
#else:
    #print("No Dicom Images were found - exiting")
    #sys.exit(5)
##########################################################################Look for images locally####################################

local_img=input("Please enter the drive and root path where the Dicom Images can be located:\n")
 
    
dcofiles=[]
dcotypes = [".dco", ".dcm"]
output = []
placeholder = []
#dicomfiles = [p for p in Path(imagelocation).rglob('*') if p.suffix in dcotypes]
dcofiles = glob.glob(local_img + '/**/*.dco' , recursive=True)
dcofiles.extend(glob.glob(local_img + '/**/*.dcm' , recursive=True))
print(dcofiles)

if not dcofiles:
    print("No DICOM images found in this location")
else:
    print("Images located, continuing")

for i in range(len(dcofiles)):
   placeholder.append(os.path.dirname(dcofiles[i]))     
   
print(placeholder)    


#from operator import itemgetter
#import itertools
#from itertools import groupby

#result =[]
#sortkeyfn = itemgetter(1)
#dcofiles.sort(key=sortkeyfn)
#print(dcofiles)

#for key,valuesiter in groupby(input, key=sortkeyfn):
    #result.append(dict(type=key, items=list(v[0] for v in valuesiter)))



#dir_groups = [list(g) for k, g in itertools.groupby(dcofiles)]
#print(dir_groups)              

output_dirs = []
for x in placeholder:
    if x not in output_dirs:
        output_dirs.append(x)
print(output_dirs)

print(output_dirs[0])

base_paths = []
for x in range(len(output_dirs)):
    base_paths.append(os.path.dirname(output_dirs[x]))
print(base_paths)

base_path = []
base_path = base_paths[0] 
print(base_path)

base_path_str = ''
base_path_str = ''.join(str(e) for e in base_path)
print(base_path_str)

loc_fn_path=input("Please enter the path where the FakePatients CSV can be located: \n")

loc_fn = ""
foundit5 = ""
loc_fn_split = ""

for root, dirs, files in os.walk(loc_fn_path):
    for file in files:
         if file.endswith('csv'):
            foundit5 = True
            loc_fn=(os.path.join(root, file))
            print(loc_fn)
            print(foundit5)
    if foundit4 == True: break     

else:
    loc_fn="" #This inelegant solution does the following: setting a value to loc in the event that no DICOM files are found - otherwise no value would be set in loc which would break the approach to create loc_split
    print("set to null")

if loc_fn != "": # If we find that loc has a value then we take the next step - splitting the loc destimation to get the path that we can use later in the code
   loc_fn_split=os.path.dirname(loc_fn)
   print(loc_fn_split)
   print("CSV has been located, moving on")
  #print(dcmtk_loc_split)
else:
    print("No CSV found - exiting")
    sys.exit(5)

###############################################################################################################################
#DICOM DUMP CODE
###############################################################################################################################
#Dicom Dump the files in the directories found to figure out what their modality type is

#out = check_output([dcmdump_loc, "+P", "008,0060", "+sd", "C:\Dicom Images\LMI Mammo\Dicom"])
#tagm="0008,0060"
#tagp="0010,0010"
#tagst="0020,000D"
#tagse="0020,000E"
#imagedata_m=[]
imagedata_stuid=[]
#imagedata_seid=[]proc_code_i = (proc_code[i]) # Parse out the Proedure Code out seperately 
#imagedata_list=[]
#imagedata_mrn=[]

#for i in output_dirs:
    #imagedata_list.append([])

#print(imagedata_m)proc_code = []
#command = [dcmdump_loc, "+P", "008,0060", "+sd", "C:\Dicom Images\LMI Mammo\Dicom"]
#tag_test='{}'.format(tagm)
#for i in range(len(output_dirs)):
    #file_dir=(output_dirs[i])
    #print(file_dir)
    #imagedata_m.append(subprocess.run([dcmdump_loc, "+P", "0008,0060", "+sd", file_dir], stdout=subprocess.PIPE).stdout.decode('utf-8'))

#print(imagedata_m)

stuid = []
for i in output_dirs:
    print(i)
    os.chdir(dcmtk_loc_split)
    stuid.append(subprocess.check_output(["dcmdump", "+P", "0020,000D", "+sd", i], encoding="utf-8"))

print(stuid)


    




stuid_num = []
for i in stuid:
    stuid_num.extend(re.findall(r'(?<=\[)[^]]+(?=\])', i)) # Get the STUID's only inside the square brackets
print(stuid_num)

from collections import Counter
_count = Counter(stuid_num)
print(_count)

for i in _count:
    common_element = _count.most_common()
print(common_element)
_count.update(stuid_num)
for a in common_element:
    print(a)

#atest = Counter(stuid_num)
#print(atest)


type(stuid_num)

stuid_clean = []
for i in stuid_num:
   stuid_clean.append(re.findall(r'(\[\d(.*?).+?\])', i))
print(stuid_clean)

(re.findall(r'(\[\d(.*?).+?\])', i))

for i in stuid_num:
    print(stuid_num[0])

study_count = []
for x in stuid_num:
    if x not in study_count:
        study_count.append(x) #Sort out the number of unique STUID's
print(study_count)



temp_plc = ''
templ_clean = ''
test =[]
for i in output_dirs:
    os.chdir(dcmtk_loc_split)
    temp_plc = (subprocess.check_output(["dcmdump", "+P", "0020,000D", "+sd", i], encoding="utf-8"))
    print(temp_plc)
    templ_clean = (re.findall(r'(?<=\[)[^]]+(?=\])', temp_plc))
    print(templ_clean)
    print(i)
    break
    set(study_count).intersection(templ_clean)
    
    
    
    [i for i, j in zip(templ_clean, study_count) if i is j]

    
    in templ_clean == study_count(i):
        print("its the same")
    print(templ_clean)
    for i in study_count:
        print('this is i', i)
        if i is templ_clean:
            print("its the same")


    
#print(imagedata_mrn)
#Filter the list image data to get only the modality types
#m=[]
#for i in imagedata_m:
    #m.append(re.findall(("MG"), i))
         

#m=[]
#for i in imagedata_m:
    #m.append(re.findall((r'\[(.*?)\]'), i))
#print(m)proc_code_i = (proc_code[i]) # Parse out the Proedure Code out seperately 


#mrn=[]
#for i in imagedata_mrn:
    #mrn.append(re.findall((r'\[(.*?)\]'), i))
#print(mrn)


#for i in m:
   # m.append[i](',')
    
#print(m)

#m_unique = [item[0] for item in m]
#print(m_unique)

#m_unique_c=','.join(m_unique)
#m_unique_c = [item for key in m_unique for item in (key, ',')] 

#print(m_unique_c)

#m_stuid=[]
#for i in range(len(output_dirs)):
    #file_dir=(output_dirs[i])
    #print(file_dir)
    #imagedata_stuid.append(subprocess.run([dcmdump_loc, "+P", "0020,000D", "+sd", file_dir], stdout=subprocess.PIPE).stdout.decode('utf-8'))
#imagedata_m.append(subprocess.run([dcmdump_loc, "+P", "008,0060", "+P", "0020,000D", "+P", "0020,000E", "+sd", file_dir], stdout=subprocess.PIPE).stdout.decode('utf-8'))
#print(imagedata_stuid)

#r = re.findall(r'(\[\d(.*?).+?\])', imagedata_stuid)
#print(r)

#m_stuid=[]
#for i in imagedata_stuid:
    #m_stuid.append(re.findall("(?<=\[).*?(?=\])", i))
#print(m_stuid)


#for i in imagedata_stuid:
   # m_stuid.append(re.findall(r'(\[\d(.*?).+?\])', i))
#print(m_stuid)

#r=datetime.datetime.now()

#m_unique_stuid=[]
#m_unique_stuid = [item[0] for item in m_stuid]
#print(m_unique_stuid)

#m_unique_stuid_c=[]asps_loc_split = []


#m_unique_stuid_c=','.join(m_unique_stuid)
#print(m_unique_stuid_c)
#m_seid=[]
#for i in range(len(output_dirs)):
    #file_dir=(output_dirs[i])
    #print(file_dir)
    #imagedata_seid.append(subprocess.run([dcproc_code_i = (proc_code[i]) # Parse out the Proedure Code out seperately 

#imagedata_m.append(subprocess.run([dcmdump_loc, "+P", "008,0060", "+P", "0020,000D", "+P", "0020,000E", "+sd", file_dir], stdout=subprocess.PIPE).stdout.decode('utf-8'))
#print(imagedata_seid)proc_code = []

#for i in imagedata_seid:
    #m_seid.append(re.findall(r'(\[\d(.*?).+?\])', i))
#print(m_seid[0])
#######################################################################################################################################




#################################################################################################
# Get the Fake Patients list from DropBox

#fn_path ='' # Path to download the document to for the Fake Names CSV file
#fn_db_path = [] # Path where the FakeNameGenerator CSV is stored on DropBox
#fn_db_path = '/Fake Patients CSV/FakeNameGenerator.com_b2e74ba1.csv'
#fn_file = ''
#fn_file = (os.path.basename(fn_db_path))

#fn_path = (imagepath + '/' + fn_file)
#print(fn_path)

#print(fn_file)
            
#try:
    #metadata = dbx.files_download_to_file(download_path=fn_path, path=fn_db_path)
#except dropbox.exceptions.PermissionError as err:
            #print('you may have the file open - please close it and try again', err)
#################################################################################################               

#Creating a random folder to copy the images to.  This is due to a bug in the deidentification tool


home = os.path.expanduser('~')
print(home)
dirname="/EditedImages"
homepath = home + dirname
print(homepath)

if os.path.exists(homepath):
    print("The path exists...now looking for images")
else:
    os.mkdir(homepath, mode=0o777)

print(stuid)

basename="/Images_"
suffix=datetime.datetime.now().strftime("%M%S")
loc_img_pth= "".join([homepath, basename,suffix])
print(loc_img_pth)
os.mkdir(loc_img_pth, mode=0o777)


#chdir_path =  "".join(dcmtk_loc_split + '/')
#print(chdir_path)

#Creating a random folder to copy the deidentified images to.  This is due to a bug in the deidentification tool
#basename="/Modified_"
#suffix=datetime.datetime.now().strftime("%H%M%S")
#modified= "_".join([basename,suffix])
#print(modified)
#os.mkdir(modified)

#Copy the images from the directory they were found in to our newly created image directory
 

############Datetime for HL7 message
#import datetime
#dt=""
#r=datetime.datetime.now()
#print(r)
#dt=(r.strftime("%Y%m%d%H%M%S"))
#print(dt)

#dt2=""
#r=datetime.datetime.now()
#print(r)
#dt=(r.strftime("%Y%m%d%H%M%S"))
#print(dt2)
#import random
#cntrl_id = random.randrange(1, 10**6)
# using format
#num_with_zeros = '{:03}'.format(cntrl_id)proc_code_i = (proc_code[i]) # Parse out the Proedure Code out seperately 
# using string's zfill
#num_with_zeros = str(cntrl_id).zfill(3)
#print(cntrl_id)
#type(cntrl_id)


#os.chdir(loc_img_pth)
#basename="ADT_A01" #this csv we will dump the data in from our list - once we remove the top element from the list - creating a new list minus the patient we used
#suffix=datetime.datetime.now().strftime("%M%S")
#temp_adt= ("_".join([basename, suffix]) + '.txt')
#print(temp_adt)
#new_adt= open(temp_adt, mode='w')
#new_adt.write('MSH|^~\&|AccMgr|1|||%s||ADT^A01|%d|P|2.4||EVN|A01|%d|||||PID|1||%s||NAME||BIRTHDAY|GENDER|1|ADDRESS|PHONE NUMBER1|Phone Number2|1|2|||||||||||||||||||||||||||||||||||PV1|1|I|' % (dt, cntrl_id, dt2, mrn_num, ))
#new_adt.close()

#from pathlib import Path #Store the location year = ''.join(str(e) for e in B_date_ordered)
#new_csv_loc=Path(temp_csv).resolve()
#print(new_csv_loc)

import shutil

#Once for dco
for file in dcofiles:
    if os.path.isfile(file):
        shutil.copy2(file, loc_img_pth)

#once for dcmGivenName = 6 
for file in dcofiles:
    if os.path.isfile(file):
        shutil.copy2(file, loc_img_pth)


#Count the number of DICOM files and store them into a list
asps = []
for root, dirs, files in os.walk(loc_img_pth):
    for file in files:
        if file.endswith((".dco", ".dcm")):
            asps.append(os.path.join(root, file))
            #print(asps)
print(asps)
 
procedure_code = []
for i in asps:
    os.chdir(dcmtk_loc_split)
    procedure_code.append(subprocess.check_output(["dcmdump", "+U8","-s", "+P", "0008,1030", "+sd", i], encoding="utf-8"))
    print(procedure_code)

proc_code = [] # Capturing Procedure Codes from the DICOM Dump
for i in procedure_code:
    proc_code.append(re.findall("(?<=\[).*?(?=\])", i))
print(proc_code)

#proc_out = [item for elem in proc_code for item in elem] # This removes the sublists and copies into a list
#print(proc_out)
   


#Establish directory of the dcmodify tool which we will use to edit the images   procedure_code.append(subprocess.check_call([dcmdump_loc, "+P", "0008,1030", "+sd", loc_img_pth]))
base_filename='dcmodify'
pfile1=os.path.join(dcmtk_loc_split, base_filename)

# Counter and list name we will use to store the CSV data to edit it
fake_patients = []

#Store the data from the csv file into a list so that we can update the list
with open(loc_fn, mode='r') as csv_file:
     csv_reader = csv.reader(csv_file)
     fake_patients = list(csv_reader) # Build List
     lines = (len(fake_patients) -1) # count number of lines in the csv
     print(lines)



#import time
#def millisuffix():
   #milliseconds = int(round(time.time() * 1000))
    #milli=str(milliseconds)[-3:]
    #return milli

#millisuffix()
#print(milli)
#import random
#mrn_num = str(random.randrange(1, 10**7))
# using format
#num_with_zeros = '{:03}'.format(mrn_num)
# using string's zfill
#num_with_zeros = str(mrn_num).zfill(3)
#print(mrn_num)
#type(mrn_num) 

#mrn_num = str(random.randrange(1, 10**7))
#num_with_zeros = str(mrn_num).zfill(3)

#Loop which will look fdef ORM:or the numb year = ''.join(str(e) for e in B_date_ordered)er of images the user which is to edit, and then count the loop based on the number of images
#For each iteration through the loop - the GivenName and Surname will be pulled form the spreadsheet and used in the edit of the images
#Then the loop will remove the first element of the list in an iterative fashion.
#Once it has reached the end of its counter, it will take the updated list with the subtracted patients, and store them in a new CSV
#We then delete the existing CSV that was used originally, and rename the new CSV the same as the original CSV
#Then we break the loop to ensure its completed

#dt, cntrl_id, dt2, mrn_num, name, year, value_Gender, full_address, P_num_out, ref_phys_name, orc2, orc2, orc9, ref_phys_name, orc2, orc2, proc_final, obr6, obr7, obr8, ref_phys_name, obr22

#mrn_num
#name
#hl7_name
#birthday
#gender
#full_address
#phone number


class Patient:
    def __init__(self):
        self.i = 0
        self.GivenName = 6
        self.Surname = 8 # Column that the Surname resides in ***Future Enhancement as above in GivenName needed
        self.B_date = 15
        self.Gender = 0
        self.Address = 2  
        self.Metro = 1
        self.State = 9  
        self.Zip = 11
        self.P_num = 13
        self.fake_patients = []
        self.name=""
        self.value_GN=''
        self.value_Sur=''
        self.mrn_num = 0
        #self.mrn = str(random.randrange(1, 10**7))
        #self.random_num = random.randint(1, lines)
        #self.name = name
        #self.hl7_name = hl7_name
        #self.birhtdate = birthdate
        #self.gender = gender
        #self.full_address = full_address
        #self.phone_num = phone_num
     
   
    def openList(self):
        with open(loc_fn, mode='r') as csv_file:
            csv_reader = csv.reader(csv_file)
            self.fake_patients = list(csv_reader) # Build List
            self.lines = (len(fake_patients) -1) # count number of lines in the csv
            
            #print(self.lines)
           
    def get_random_num(self):
        self.openList()
        self.random_num = random.randint(1, self.lines)
        #print(self.random_num)
  
     
    def patient_name(self):
        self.get_random_num()
        #print(self.GivenName)
        #self.openList()
        #self.get_random_num()
        for i in self.fake_patients:
            value_GN = str(self.fake_patients[self.random_num][self.GivenName])
            value_Sur = str(self.fake_patients[self.random_num][self.Surname])
            name = value_GN + " " + value_Sur #
            self.hl7_name = value_Sur + "^" + value_GN # This formats the name variable into a HL7 suitable format
            break
        #print(value_GN)
        #print(value_Sur)
        #print(name)
        #print(self.hl7_name)
    
    def get_mrn(self):
        self.mrn_num = str(random.randrange(1, 10**7))
        #print(self.mrn_num)
       
    def birthdate_hl7(self):
        for i in self.fake_patients:
            value_B_date = str(self.fake_patients[self.random_num][self.B_date])
            B_date_split=value_B_date.split("/")
            break
        for z in range(0, len(B_date_split)): # taking the birthdate and then splitting it, and re-arranging it into the format required for HL7
            B_date_split[z] = int(B_date_split[z])
        B_date_split = ["%02d" % n for n in B_date_split]
        date_order = [2, 0, 1]
        B_date_ordered = [B_date_split[t] for t in date_order]
        self.year = ''.join(str(e) for e in B_date_ordered) # Turn list into string
        #print(self.year)
    
    def get_address(self):
        for i in self.fake_patients:
             value_Address = str(self.fake_patients[self.random_num][self.Address])
             value_City = str(self.fake_patients[self.random_num][self.Metro])
             value_State = str(self.fake_patients[self.random_num][self.State])
             value_Zip = str(self.fake_patients[self.random_num][self.Zip])
             break
        self.full_address = (value_Address + "^^" + value_City + "^" + value_State + "^" + value_Zip)
        #print(self.full_address) 
    
    def get_phonenum(self):
        for i in self.fake_patients:
            value_P_num = str(self.fake_patients[self.random_num][self.P_num])
            P_num_split = value_P_num.split("-") # P_num is for phone number
            self.P_num_out = ''.join(p for p in P_num_split)
            break
        #print(self.P_num_out)
        
    def get_gender(self):
        for i in self.fake_patients:
            self.value_Gender = str(self.fake_patients[self.random_num][self.Gender])
            break
        #print(self.value_Gender)



class Hl7_Messages:
    def __init__(self):
        self.adt_basename ="ADT_A01" #this csv we will dump the data in from our list - once we remove the top element from the list - creating a new list minus the patient we used
        self.orm_basename = "ORM_O01"
        self.dt = ""
        self.dt2 = ""
        self.orc9 = ""
        self.obr6 = ""
        self.obr7 = ""
        self.obr8 = ""
        self.obr22 = "" 
        self.obr25 = "F"
        self.obr32 = "1142&Zaphod&Beeblebrox"
        obj = Patient()
        obj.get_mrn()
        obj.patient_name()
        obj.get_phonenum()
        obj.birthdate_hl7()
        obj.get_address()
        obj.get_gender()
        self.msg_mrn = obj.mrn_num
        self.msg_name = obj.hl7_name
        self.msg_bdate = obj.year
        self.msg_address = obj.full_address
        self.msg_phone_num = obj.P_num_out
        self.msg_gender = obj.value_Gender
        self.GivenName = 6
        self.Surname = 8 
     
    def get_random_minutes(self):
     self.x = int(random.randrange(1, 59))
          
     
    def get_random_hours(self):
     self.y = int(random.randrange(8, 18))
    
    
    def get_milliseconds(self):
     milliseconds = int(round(time.time() * 1000))
     self.milli = str(milliseconds)[-3:]
    
    
    def current_datetime(self):
     r = datetime.datetime.now()
     self.dt = (r.strftime("%Y%m%d%H%M%S"))
      
     
    def datetime2(self):
     self.get_random_minutes()
     q = datetime.datetime.now()
     q_plus_1hr = q + datetime.timedelta(hours = 1)
     self.dt2 = (q_plus_1hr.strftime("%Y%m%d%H%M%S"))
     w_plus_x = q + datetime.timedelta(hours = 1, minutes = self.x)
     self.orc9 = (w_plus_x.strftime("%Y%m%d%H%M%S"))
     if self.x <= 50:
        self.x += 10
        z_plus_1hr = q + datetime.timedelta(hours = 1, minutes = self.x)
        self.obr6 = (z_plus_1hr.strftime("%Y%m%d%H%M%S"))
     else:
        z_plus_1hr = q + datetime.timedelta(hours = 2, minutes = self.x)
        self.obr6 = (z_plus_1hr.strftime("%Y%m%d%H%M%S"))
     print(self.obr6)
     self.get_random_minutes()
     v_plus_3hr = z_plus_1hr + datetime.timedelta(hours = 3, minutes = self.x)
     self.obr7 = (v_plus_3hr.strftime("%Y%m%d%H%M%S "))
     print(self.obr7)
     b_plus_4hr = v_plus_3hr + datetime.timedelta(hours = 4)
     obr8 = (b_plus_4hr.strftime("%Y%m%d%H%M%S "))
     self.get_random_hours()
     b_plus_12hr = v_plus_3hr + datetime.timedelta(hours = self.y)
     self.obr22 = (b_plus_12hr.strftime("%Y%m%d%H%M%S "))
     print(self.obr22)
   
    
    def get_ref_phys(self):
        obj = Patient()
        obj.get_random_num()
        for i in obj.fake_patients:
            random_num_ref1 = (random.randrange(1, obj.lines)) # For random first name to create a random referring physician name
            random_num_ref2 = (random.randrange(1, obj.lines)) # for a random last name to create a random referring physician name
            value_refphys_given = str(fake_patients[random_num_ref1][self.GivenName])
            value_refphys_sur = str(fake_patients[random_num_ref2][self.Surname])
            ref_phys_num = str(random.randrange(1, 10**4))
            self.ref_phys_name = ref_phys_num + "^" + value_refphys_sur + "^" + value_refphys_given
            break
        print(self.ref_phys_name)


    def control_id(self):
     self.cntrl_id = random.randrange(1, 10**6)
     num_with_zeros = '{:03}'.format(self.cntrl_id)
     num_with_zeros = str(self.cntrl_id).zfill(3)
     
     
    def get_accession_num(self):
     self.orc2 = str(random.randrange(1, 10**8))
     #num_with_zeros = str(self.orc2).zfill(3)
     print(self.orc2)


    def ADT_A01(self):
     self.control_id()
     self.current_datetime()
     self.datetime2()
     obj = Patient()
     obj.get_random_num()
     obj.patient_name()
     obj.birthdate_hl7()
     obj.get_gender()
     obj.get_address()
     obj.get_phonenum()
     self.get_milliseconds()
     suffix = datetime.datetime.now().strftime("%S")
     temp_adt= ("_".join([self.adt_basename, suffix]) + self.milli + '.txt')
     print(temp_adt)
     print(self.msg_mrn)
     #print(self.cntrl_id)
     #print(obj.random_num)
     os.chdir(loc_img_pth) 
     new_adt= open(temp_adt, mode='w')
     new_adt.write(f'MSH|^~\&|AccMgr|ScriptSend|||{self.dt}||ADT^A01|{self.cntrl_id}|P|2.4||EVN|A01|{self.dt2}|||||PID|1||{self.msg_mrn}||{self.msg_name}||{self.msg_bdate}|{self.msg_gender}|1|{self.msg_address}|{self.msg_phone_num}||1|2|||||||||||||||||||||||||||||||||||PV1|1|I|')# % (dt, cntrl_id, dt2, mrn_num, hl7_name, year, value_Gender, full_address, P_num_out))
        #new_adt.close()
 
    def ORM_O01(self):
     self.get_milliseconds()
     self.control_id()
     self.get_ref_phys()
     self.datetime2()
     self.get_accession_num()
     print(self.milli)
     #suffix = datetime.datetime.now().strftime("%S")
     temp_orm= ("_".join([self.orm_basename] ) + "_" + self.milli + '.txt')
     print(temp_orm)
     #print(self.mrn_num)
     print(self.msg_mrn)
     new_orm= open(temp_orm, mode='w')
     new_orm.write(f'MSH|^~\&|ScriptSend|KaizentixTester^9999^MOH|Interlinx|KaizentixCloud|{self.dt}||ORM^O01|{self.cntrl_id}|P^T|2.4|PID|||{self.msg_mrn}||{self.msg_name}||{self.msg_bdate}|{self.msg_gender}|||{self.msg_address}||{self.msg_phone_num}|PV1||O||||||{self.ref_phys_name}|ORC|NW|{self.orc2}|{self.orc2}||CM||||{self.orc9}|||{self.ref_phys_name}|||||Kaizentixtester^9999|OBR|1|{self.orc2}|{self.orc2}|proc_final||{self.obr6}|{self.obr7}|{self.obr8}||||||||{self.ref_phys_name}||||||{self.obr22}|||F|||||||{self.obr32}|') #% (dt, cntrl_id, dt2, mrn_num, name, year, value_Gender, full_address, P_num_out, ref_phys_name, orc2, orc2, orc9, ref_phys_name, orc2, orc2, proc_final, obr6, obr7, obr8, ref_phys_name, obr22,))
     #new_orm.close()
     



hl7obj = Hl7_Messages()

hl7obj.datetime2()

hl7obj.ADT_A01()
hl7obj.ORM_O01()
hl7obj.get_ref_phys()
obj = Patient()
obj.openList()
obj.get_random_num()
obj.patient_name()
obj.get_mrn()
obj.birthdate_hl7()
obj.get_address()
obj.get_phonenum()
obj.get_gender()


    
#dt, cntrl_id, dt2, mrn_num, hl7_name, year, value_Gender, full_address, P_num_out  

x = int(random.randrange(20, 59))
print(x)


   # def ORM():

     #obr6 = ""
     #z = datetime.datetime.now()
     #z_plus_1hr = z + datetime.timedelta(hours = 1, minutes = x)
     #obr6 = (z_plus_1hr.strftime("%Y%m%d%H%M%S"))
     #print(obr6)
     #obr7 = ""
     #v_plus_3hr = z + datetime.timedelta(hours = 3)
     #obr7 = (v_plus_3hr.strftime("%Y%m%d%H%M%S "))
     #print(obr7)
     #obr8 = ""   
     #b_plus_4hr = z + datetime.timedelta(hours = 4)
     #obr8 = (b_plus_4hr.strftime("%Y%m%d%H%M%S "))
     #print(obr8)
     #obr22 = "" 
     #a = datetime.datetime.now()
     #b_plus_12hr = a + datetime.timedelta(hours = 10)
     #obr22 = (b_plus_12hr.strftime("%Y%m%d%H%M%S "))
     #print(obr22)
     #obr25 = "F"
     #obr32 = "1142&Zaphod&Beeblebrox"
     #milliseconds = int(round(time.time() * 1000))
     #milli=str(milliseconds)[-3:]
     #suffix=datetime.datetime.now().strftime("%S")
     #temp_orm= ("_".join([ORM_basename, suffix]) + milli + '.txt')
     #print(temp_orm)
     #new_orm= open(temp_orm, mode='w')
     #new_orm.write(f'MSH|^~\&|ScriptSend|KaizentixTester^9999^MOH|Interlinx|KaizentixCloud|{dt}||ORM^O01|{cntrl_id}|P^T|2.3.1|PID|||{mrn_num}||{hl7_name}||{year}|{value_Gender}|||{full_address}||{P_num_out}|PV1||O||||||{ref_phys_name}|ORC|NW|{orc2}|{orc2}||CM||||{orc9}|||{ref_phys_name}|||||Kaizentixtester^9999|OBR|1|{orc2}|{orc2}|{proc_final}||{obr6}|{obr7}|{obr8}||||||||{ref_phys_name}||||||{obr22}|||F|||||||{obr32}|') #% (dt, cntrl_id, dt2, mrn_num, name, year, value_Gender, full_address, P_num_out, ref_phys_name, orc2, orc2, orc9, ref_phys_name, orc2, orc2, proc_final, obr6, obr7, obr8, ref_phys_name, obr22,))
     #new_orm.close()
     
    #def import_list():
        #print("Crap")
        #with open(loc_fn, mode='r') as csv_file:
            #csv_reader = csv.reader(csv_file)
           # for row in csv_reader:
                #random_num=random.randint(1, lines)
                #value_GN = str(fake_patients[random_num][GivenName])
                #value_Sur = str(fake_patients[random_num][Surname]) # Same as above but for Surname
                #value_B_date = str(fake_patients[random_num][B_date])
                #value_Gender = str(fake_patients[random_num][Gender])
                #value_Address = str(fake_patients[random_num][Address])
                #value_City = str(fake_patients[random_num][Metro])
                #value_P_num = str(fake_patients[random_num][P_num])
                #value_State = str(fake_patients[random_num][State])
                #value_Zip = str(fake_patients[random_num][Zip])
                #random_num_ref1 = (random.randrange(1, lines)) # For random first name to create a random referring physician name
                #random_num_ref2 = (random.randrange(1, lines)) # for a random last name 
                #print(random_num)
                #print(GivenName)
                #print(value_GN)
                #print(value_Sur)
                #break
q = datetime.datetime.now()
x = int(random.randrange(15, 59))
w_plus_10 = q + datetime.timedelta(hours = 1, minutes = x)
orc9 = (w_plus_10.strftime("%Y%m%d%H%M%S"))
if x <= 50:
    x += 10
    z_plus_1hr = q + datetime.timedelta(hours = 1, minutes = x)
    obr6 = (z_plus_1hr.strftime("%Y%m%d%H%M%S"))
    print("I added 10 mins")
else:
    z_plus_1hr = q + datetime.timedelta(hours = 2, minutes = x)
    obr6 = (z_plus_1hr.strftime("%Y%m%d%H%M%S"))
    print("I added the 2 hours")
   
print(obr6)
v_plus_3hr = z_plus_1hr + datetime.timedelta(hours = 3)
obr7 = (v_plus_3hr.strftime("%Y%m%d%H%M%S "))
print(obr7)



Patient.get_random_num()
Patient.openList(1)
Patient.a_test()

      #self.openList()
        #self.random_num = random.randint(1, self.lines)
        #print(self.random_num)




test = []
print(Patient.get_random_num(mrn_num))
name = Patient()
name.import_list()
Patient.import_list()
p = Patient()
p.get_mrn()
p.get_random_num()
p.get_name()
Patient.get_mrn(p)



b = birthdate_hl7()
b.birthdate_hl7()
print(b.year)
print(b)

def ORM():
    ORM_basename = "ORM_O01"
    #ORM_basepatient_id_lst = name= #this csv we will dump the data in from our list - once we remove the top element from the list - creating a new list minus the patient we used
    orc2 = str(random.randrange(1, 10**8))
    num_with_zeros = str(orc2).zfill(3)
    patient_id_lst.extend(orc2)
    print(orc2)
    orc9 = ""
    w = datetime.datetime.now()
    w_plus_10 = w + datetime.timedelta(minutes = 10)
    orc9 = (w_plus_10.strftime("%Y%m%d%H%M%S"))
    obr6 = ""
    z = datetime.datetime.now()
    z_plus_1hr = z + datetime.timedelta(hours = 1)
    obr6 = (z_plus_1hr.strftime("%Y%m%d%H%M%S"))
    print(obr6)
    obr7 = ""
    v_plus_3hr = z + datetime.timedelta(hours = 3)
    obr7 = (v_plus_3hr.strftime("%Y%m%d%H%M%S "))
    print(obr7)
    obr8 = ""   
    b_plus_4hr = z + datetime.timedelta(hours = 4)
    obr8 = (b_plus_4hr.strftime("%Y%m%d%H%M%S "))
    print(obr8)
    obr22 = "" 
    a = datetime.datetime.now()
    b_plus_12hr = a + datetime.timedelta(hours = 10)
    obr22 = (b_plus_12hr.strftime("%Y%m%d%H%M%S "))
    print(obr22)
    obr25 = "F"
    obr32 = "1142&Zaphod&Beeblebrox"
    milliseconds = int(round(time.time() * 1000))
    milli=str(milliseconds)[-3:]
    suffix=datetime.datetime.now().strftime("%S")
    temp_orm= ("_".join([ORM_basename, suffix]) + milli + '.txt')
    print(temp_orm)
    new_orm= open(temp_orm, mode='w')
    new_orm.write(f'MSH|^~\&|ScriptSend|KaizentixTester^9999^MOH|Interlinx|KaizentixCloud|{dt}||ORM^O01|{cntrl_id}|P^T|2.3.1|PID|||{mrn_num}||{hl7_name}||{year}|{value_Gender}|||{full_address}||{P_num_out}|PV1||O||||||{ref_phys_name}|ORC|NW|{orc2}|{orc2}||CM||||{orc9}|||{ref_phys_name}|||||Kaizentixtester^9999|OBR|1|{orc2}|{orc2}|{proc_final}||{obr6}|{obr7}|{obr8}||||||||{ref_phys_name}||||||{obr22}|||F|||||||{obr32}|') #% (dt, cntrl_id, dt2, mrn_num, name, year, value_Gender, full_address, P_num_out, ref_phys_name, orc2, orc2, orc9, ref_phys_name, orc2, orc2, proc_final, obr6, obr7, obr8, ref_phys_name, obr22,))
    new_orm.close()

def current_datetime():
      dt = ""
      r = datetime.datetime.now()
      dt = (r.strftime("%Y%m%d%H%M%S"))

def current_datetime2():
     dt2=""
     q=datetime.datemrn_numtime.now()
     dt2=(q.strftime("%Y%m%d%H%M%S"))
     
def control_id():
    cntrl_id = random.randrange(1, 10**6)
    num_with_zeros = '{:03}'.format(cntrl_id)
    num_with_zeros = str(cntrl_id).zfill(3)

def phone_number():
    P_num_split=value_P_num.split("-") # P_num is for phone number
    print(P_num_split)
    P_num_out = ''.join(p for p in P_num_split)
    print(P_num_out)

def ADT_A01():
     basename="ADT_A01" #this csv we will dump the data in from our list - once we remove the top element from the list - creating a new list minus the patient we used
     milliseconds = int(round(time.time() * 1000))
     milli=str(milliseconds)[-3:]
     suffix=datetime.datetime.now().strftime("%S")
     temp_adt= ("_".join([basename, suffix]) + milli + '.txt')
     patient_id_lst.extend([name, mrn_num, full_address, P_num_out, ref_phys_name])
     print(temp_adt)
     new_adt= open(temp_adt, mode='w')
     new_adt.write('MSH|^~\&|AccMgr|ScriptSend|||%s||ADT^A01|%d|P|2.4||EVN|A01|%s|||||PID|1||%s||%s||%s|%s|1|%s|%s||1|2|||||||||||||||||||||||||||||||||||PV1|1|I|' % (dt, cntrl_id, dt2, mrn_num, hl7_name, year, value_Gender, full_address, P_num_out))
     new_adt.close()

def procedure_code():
    proc_code_i = (proc_code[i]) # Parse out the Proedure Code out seperately 
    proc_code_str = ''.join(r for r in proc_code_i) # Turn the Procedure Code into a string
    print(proc_code_str)
    proc_split = proc_code_str.split(" ")
    print(proc_split)
    proc_carrot = '^'.join(p for p in proc_split)
    print(proc_carrot)
    proc_num = str(random.randrange(1, 10**4))
    print(proc_num)
    proc_final = proc_num + '^' + proc_carrot
    print(proc_final)

#MSH|^~\&|ScriptSend|KaizentixTester^9999^MOH|Interlinx|KaizentixCloud|%s(dt)||ORM^O01|%d(cntrl_id)|P^T|2.3.1|
#PID|||%s(MRN)||%s(name)||%s(b-day)|%s(Gender)|||%s(address)||%s(Phone Number)|PV1||O||||||%s(ref_phys_name)|
#ORC|NW|%d (orc2)|%d (orc2)||CM||||%d(orc9)|||%s(ref_phys_name|||||Kaizentixtester^9999|
#OBR|1|%d(orc2)|%d(orc2)| %s(proc_final)||%d(obr6)|%d(obr7)|%d(obr8)|||||||
#|%s(ref_phys_name)||||||%d(obr22)|||F|||||||1234&JONES&MARK|

mrn_list = []
patient_id_lst = [] 
i = 0
GivenName = 6 # Column that the Given Name resides in.  *p = Patient()
Surname = 8 # Column that the Surname resides in ***Future Enhancement as above in GivenName needed
B_date = 15
Gender = 0
Address = 2  
Metro = 1
State = 9  
Zip = 11
P_num = 13
year=''
full_address = ''
modify = 'dcmodify'
b = birthdate_hl7()

with open(loc_fn, mode='r') as csv_file:
     csv_reader = csv.reader(csv_file)
     for row in csv_reader:
         if i < len(asps): # if i is less than the number of images in the directory specified then do the below
             print(i)
             C #We generate a random number between 1 and the number lines that we calculated the CSV to be
             #fake_patients = list(csv_reader)
             mrn_num = str(random.randrange(1, 10**7))
             num_with_zeros = str(mrn_num).zfill(3) # Parse out the Proedure Code out seperately 
             print(mrn_num)
             value_GN = str(fake_patients[random_num][GivenName]) # Store the value in value1 determined by using our random number to tell us the row number we will pull the data from - and then use the GivenName column number to get the value - this gives us the GivenName 
             value_Sur = str(fake_patients[random_num][Surname]) # Same as above but for Surname
             value_B_date = str(fake_patients[random_num][B_date])
             value_Gender = str(fake_patients[random_num][Gender])
             value_Address = str(fake_patients[random_num][Address])
             value_City = str(fake_patients[random_num][Metro])
             value_P_num = str(fake_patients[random_num][P_num])
             value_State = str(fake_patients[random_num][State])
             value_Zip = str(fake_patients[random_num][Zip])
             random_num_ref1 = (random.randrange(1, lines)) # For random first name to create a random referring physician name
             random_num_ref2 = (random.randrange(1, lines)) # for a random last name to create a random referring physician name
             value_refphys_given = str(fake_patients[random_num_ref1][GivenName])
             value_refphys_sur = str(fake_patients[random_num_ref2][Surname])
             ref_phys_num = str(random.randrange(1, 10**4))
             ref_phys_name = ref_phys_num + "^" + value_refphys_sur + "^" + value_refphys_given
             print(ref_phys_name)
             print(value_GN,value_Sur)
             name = value_GN + " " + value_Sur #Concatonate the two values together to give us a firstname and lastname
             print(name)
             hl7_name = value_Sur + "^" + value_GN # This formats the name variable into a HL7 suitable format
             print(hl7_name)
             print(value_B_date)
             birthdate_hl7()
             full_address = (value_Address + "^^" + value_City + "^" + value_State + "^" + value_Zip)
             current_datetime()
             current_datetime2()
             control_id()
             phone_number
             os.chdir(loc_img_pth) 
             ADT_A01()
             print(proc_code)
             procedure_code()
             ORM()
             edit_it = (asps[i]) # We stored the location of the images above in a list.  This simply pulls the image from the list correspinding to its value - which is based on our counter = i.  for every trip through the loop - i will goup by one, which will then pull the next image in the list.
             print(edit_it)
             name_go = '(0010,0010)={}'.format(name) # This was required to turn the name value into a string which is recognized by the command line subprocess call
             mrn_go = '(0010,0020)={}'.format(mrn_num)
             i += 1 # counter
             print(i)
             print("Finished ADT Stuff")
             os.chdir(dcmtk_loc_split)
             subprocess.check_call([modify, "-gst", "-ma", name_go,  "-ma", mrn_go, edit_it])
             subprocess.check_output(["dcmsend", "-aec", "INTERLINX_SCP", "localhost", "43022", edit_it])
             #subprocess.check_call(["dcmodify", "-gst", "-ma", name_go, "-ma", mrn_go, edit_it],shell=True) #subprocess call which calls the dcmmodify.exe program to start the modification and feeds it the parameters including the patient name
             print("Completed image edit", i)
             
         #else:
             #print("Your images have been updated with the supplied data.")
             #print("The edited images can be found in ", imagepath)
             #break
             #with open(new_csv_loc, mode='w', newline='') as new_csv:
                     #csv_file.close()
                     #header = ['ï»¿Gender', 'City', 'StreetAddress', 'Number', 'NameSet', 'Title', 'GivenName', 'MiddleInitial', 'Surname', 'State', 'StateFull', 'ZipCode', 'Country', 'TelephoneNumber', 'TelephoneCountryCode', 'Birthday', 'NationalID', 'Kilograms', 'Centimeters']
                     #writer1 = csv.DictWriter(new_csv, fieldnames = header)
                     #writer1.writeheader()
                     #os.chdir(imagepath)
                     #writer1.writerows(fake_patients)
                     #new_csv.close()
                     #os.remove(datadir)
                     #os.rename(new_csv_loc, datadir)
                     #print("Your images have been updated with the supplied data.")
                     #print("The edited images can be found in ", imagepath)
                     #break
             









