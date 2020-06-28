import os, sys, glob, random, csv, subprocess, datetime, re, fnmatch, itertools, zipfile
from pathlib import Path
from subprocess import check_output

import dropbox
from dropbox import DropboxOAuth2FlowNoRedirect
from dropbox.files import WriteMode

'''
This example walks through a basic oauth flow using the existing long-lived token type
Populate your app key and app secret in order to run this locally
'''
##APP_KEY = "a90oqmyed5wnmh9" #This was the test App Key
#APP_SECRET = "iljg7hejagotif9" # Test App Secret
#APP_KEY = "ug87411834vwptu"
#APP_SECRET = "mcvivu0po9uefxq"

#auth_flow = DropboxOAuth2FlowNoRedirect(APP_KEY, APP_SECRET)

#authorize_url = auth_flow.start()
#print("1. Go to: " + authorize_url)
#print("2. Click \"Allow\" (you might have to log in first).")
#print("3. Copy the authorization code.")
#auth_code = input("Enter the authorization code here: ").strip()

#try:
    #oauth_result = auth_flow.finish(auth_code)
#except Exception as e:
    #print('Error: %s' % (e,))
    #exit(1)

#dbx = dropbox.Dropbox(oauth2_access_token=oauth_result.access_token)
#dbx.users_get_current_account()
#print("Successfully set up client!")


#token="RnjGR8eO64AAAAAAAAAAIEobTanC3ZsUYse6BtUv7K0mcyQ1-EfChcfSd3V6kSls"
#Dropbox = dropbox.Dropbox
#my_client=Dropbox(token)
#folderfile_list = my_client.files_list_folder('', True, True)
#print(folderfile_list)

dbx = dropbox.Dropbox(oauth2_access_token = "5jFBH0RV7vEAAAAAAAAAYklynU3GbHW17xRqSMAcKxyiwaulcz6FUvKv0ayeAeLd")
result = dbx.files_list_folder("", recursive=True)
file_names = [] # File name only - entry.name
file_list = [] # File list - including directories - this is entry.path_lower
dcm_files = [] # DICOM file only - just in case we need it
dcm_dirs = [] # path_ower by Drop Box Standards - full path and filename
dcm_path = [] # Full path - NO filename
dcm_path_uq = [] # Unique path of the Dicom Images on DropBox
imagedata_dbm = [] # Image data DropBox - Modality data only
dump_path_dbm = [] # DICOM Dump path placeholder - when iterating over the unique directory name - store i (the directory name) in this variable so it can be called in the Dicom Dump command line
csv_path ='/master csv/master_csv.csv'
csv_file = () #This will be the variable that will house the file name itself
modalities = []
m_clean = [] # Designed to hold the extraction value of the modaity names from the directories in a non-sub-listed format
dir_groups = [] # Purpose is to group the directories into sublists to then len them to find the image counts
image_counts = [] # Exported len values to determine the image counts in each directory
m_clean_uq = []
print(result)
def process_entries(entries):
    for entry in entries:
        if isinstance(entry, dropbox.files.FileMetadata):
            file_list.append(entry.path_lower)
            file_names.append(entry.name)
            


process_entries(result.entries)
print(file_list)
print(file_names)

while result.has_more:
    result = dbx.files_list_folder_continue(result.cursor)

    process_entries(result.entries)

#print(len(file_list))

print(file_list)

for i in file_names:
    if i.endswith(('.dco', '.dcm')):
        dcm_files.append(i)

print(dcm_files)    

for i in csv_path[0]:
    csv_file = (os.path.basename(csv_path))

print(csv_file)

for i in file_list:
    if i.endswith(('.dco', '.dcm')):
        dcm_dirs.append(i)    

for i in file_list:
    if i.endswith(('.dco', '.dcm')):
        dcm_dirs.append(i)    


print(dcm_dirs)

len(dcm_files)

for i in range(len(dcm_dirs)):
    dcm_path.append(os.path.dirname(dcm_dirs[i]))

print(dcm_path)

for x in dcm_path:
    if x not in dcm_path_uq:
        dcm_path_uq.append(x)
print(dcm_path_uq)


for i in dcm_dirs:   # Take the modality type out of the directory structure and append it to the modalities list.
    if re.findall(r'(mg)', i): # for reasons unknown to me this results in a sublist of modalities - which is problematic to extract later
       modalities.append(re.findall('(mg)',i))
    elif re.findall(r'(us)',i):
       modalities.append(re.findall('(us)',i))
    elif re.findall(r'(dx)', i):
       modalities.append(re.findall(r'dx',i))
    elif re.findall(r'(ct)', i):
       modalities.append(re.findall(r'(ct)',i))

# For some unknown reason - the loop above will create a sublist for each instance it finds.  This section moves the items from the sublists to a list which is easier to extract later without the []
for elem in modalities:
    for item in elem:
        m_clean.append(item)
print(m_clean)

m_clean_uq = []
for x in m_clean:
    if x not in m_clean_uq:
        m_clean_uq.append(x)

print(m_clean_uq)                          

dir_groups = [list(g) for k, g in itertools.groupby(dcm_path)] # this will group the directories into sublists so that we can then determine
print(dir_groups)                                              # how many images are in each directory

image_counts = [] 
for i in dir_groups:
    image_counts.append(len(i)) # len which will count the number of instances of a directory and that will provide the number of images

print(image_counts)

#for entry in entries:
    #if isinstance(entry, dropbox.files.FileMetadata):  # this entry is a file
        #md, res = dbx.files_download(entry.path_lower)
        #print(md)  # this is the metadata for the downloaded file
        #print(len(res.content))  # `res.content` contains the file data

#dbx.files_download(csv_path)


# ----Create somewhat random new directory for the images
import datetime
basename="/Images_"
suffix=datetime.datetime.now().strftime("%M%S")
imagepath= "_".join([basename,suffix])
print(imagepath)
os.mkdir(imagepath)


d_path=(imagepath + '/' + csv_file)
print(d_path)
#with open(download_path, mode='w') as f:
   #res = dbx.files_download_to_file(d_path, csv_path)


try:
    metadata = dbx.files_download_to_file(download_path=d_path, path=csv_path)
except dropbox.exceptions.PermissionError as err:
            print('you may have the file open - please close it and try again', err)

with open(d_path, mode='w', newline='') as write_csv:
                     writer = csv.writer(write_csv)
                     writer.writerow(("Modality", "Image Location", "Image Counts"))
                     for i in range(len(dcm_path_uq)):
                         writer.writerow((m_clean_uq[i], dcm_path_uq[i], image_counts[i]))
                     

with open(d_path, 'rb') as f:
            dbx.files_upload(f.read(), csv_path, mode = WriteMode('overwrite'))
            
print('CSV file updated with the currentl list of studies in DropBox, and re-uploaded')


i_s = int(input("Please enter the number of studies you would like to send:\n"))

m_select=[]
with open(d_path, mode='r') as csv_file:
     csv_reader = csv.reader(csv_file)
     m_select = list(csv_reader) # Build List
     lines = (len(m_select) -1) # count number of lines in the csv
     print(lines)

print(m_select)
test_counter = int(0)
image_counter = int(0)
studies_selected = i_s
q = 0
list_modality = 0 # Column that the modality list resides in which we want to pull randomly from ***Future Enhancement - scan the list to find the location of Given Name and update the value in this variable
list_image_location = 1 # Column that the identifies the dropbox directory that the images reside in ***Future Enhancement as above in GivenName needed
list_image_counts = 2 # Column that identifies the number of images in the directory
d_holder = []
dload_zip_locs = []
zipbasename='Imagefile'    
with open(d_path, mode='r') as csv_file:
     csv_reader = csv.reader(csv_file)
     for row in csv_reader:
         if i_s > 0:
             random_num=random.randint(1, lines)
             print('random number is', random_num)
             v1 = (m_select[random_num][list_modality])
             v2 = (m_select[random_num][list_image_location])
             v3 = int(m_select[random_num][list_image_counts])
             print(v1)
             print(v2)
             print(v3)
             image_counter += v3
             update_suffix=(datetime.datetime.now().strftime("%M%S"))
             print(update_suffix)
             image_dload_path=(imagepath + '/' + update_suffix)
             os.mkdir(image_dload_path)
             print(image_dload_path)
             zip_name = ("_".join([zipbasename,update_suffix]))
             print(zip_name)
             zip_fullpath = (image_dload_path + '/' + zip_name + '.zip')
             print(zip_fullpath)
             #temp=dbx.files_list_folder(v2)
             metadata = dbx.files_download_zip_to_file(download_path=zip_fullpath, path=v2)
             dload_zip_locs.append(zip_fullpath)
             print(dload_zip_locs)
             with zipfile.ZipFile(zip_fullpath, 'r') as zip_handler:
                 zip_handler.extractall(image_dload_path)   
                 #for file in temp.entries:
                 #d_holder = v2
                 #d_name = file.name 
                 #print(d_name)
                 #metadata = dbx.files_download_zip_to_file(download_path=image_dload_path + '/' + zip_name, path=d_holder)
                 #metadata = dbx.files_download_to_file(download_path=image_dload_path + '/' + d_name, path=d_holder)
             print('downloaded')
             test_counter += 1
             print(test_counter, ' loop completed')
             print('image counter is at ', image_counter)
             i_s -= 1
           
                
print('Your images have been successfully downloaded.  A total of', image_counter, 'images were dowloaded from', studies_selected, 'studies:\n')            
        

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
   print("DCMTK tools have been located, moving on")
  #print(dcmtk_loc_split)
else:
    print("No DCMTK tools were found - exiting")
    sys.exit(5)





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
#imagedata_stuid=[]
#imagedata_seid=[]
#imagedata_list=[]
#imagedata_mrn=[]

#for i in output_dirs:
    #imagedata_list.append([])

#print(imagedata_m)
#command = [dcmdump_loc, "+P", "008,0060", "+sd", "C:\Dicom Images\LMI Mammo\Dicom"]
#tag_test='{}'.format(tagm)
#for i in range(len(output_dirs)):
    #file_dir=(output_dirs[i])
    #print(file_dir)
    #imagedata_m.append(subprocess.run([dcmdump_loc, "+P", "0008,0060", "+sd", file_dir], stdout=subprocess.PIPE).stdout.decode('utf-8'))

#print(imagedata_m)

#for i in range(len(output_dirs)):
    #file_dir=(output_dirs[i])
    #print(file_dir)
    #imagedata_mrn.append(subprocess.run([dcmdump_loc, "+P", "0010,0020", "+sd", file_dir], stdout=subprocess.PIPE).stdout.decode('utf-8'))

#print(imagedata_mrn)
#Filter the list image data to get only the modality types
#m=[]
#for i in imagedata_m:
    #m.append(re.findall(("MG"), i))
             

#m=[]
#for i in imagedata_m:
    #m.append(re.findall((r'\[(.*?)\]'), i))
#print(m)

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


#m_unique_stuid=[]
#m_unique_stuid = [item[0] for item in m_stuid]
#print(m_unique_stuid)

#m_unique_stuid_c=[]
#m_unique_stuid_c=','.join(m_unique_stuid)
#print(m_unique_stuid_c)
#m_seid=[]
#for i in range(len(output_dirs)):
    #file_dir=(output_dirs[i])
    #print(file_dir)
    #imagedata_seid.append(subprocess.run([dcmdump_loc, "+P", "0020,000E", "+sd", file_dir], stdout=subprocess.PIPE).stdout.decode('utf-8'))
#imagedata_m.append(subprocess.run([dcmdump_loc, "+P", "008,0060", "+P", "0020,000D", "+P", "0020,000E", "+sd", file_dir], stdout=subprocess.PIPE).stdout.decode('utf-8'))
#print(imagedata_seid)

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
import datetime, time




basename="/Images_"
suffix=datetime.datetime.now().strftime("%M%S")
loc_img_pth= "".join([base_path,basename,suffix])
print(loc_img_pth)
os.mkdir(loc_img_pth, mode=0o777)


#Creating a random folder to copy the deidentified images to.  This is due to a bug in the deidentification tool
#basename="/Modified_"
#suffix=datetime.datetime.now().strftime("%H%M%S")
#modified= "_".join([basename,suffix])
#print(modified)
#os.mkdir(modified)

#Copy the images from the directory they were found in to our newly created image directory
 
import shutil

#Once for dco
for file in dcofiles:
    if os.path.isfile(file):
        shutil.copy2(file, loc_img_pth)

#once for dcm
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
#num_with_zeros = '{:03}'.format(cntrl_id)
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

#from pathlib import Path #Store the location
#new_csv_loc=Path(temp_csv).resolve()
#print(new_csv_loc)




#Establish directory of the dcmodify tool which we will use to edit the images
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

#Loop which will look for the number of images the user which is to edit, and then count the loop based on the number of images
#For each iteration through the loop - the GivenName and Surname will be pulled form the spreadsheet and used in the edit of the images
#Then the loop will remove the first element of the list in an iterative fashion.
#Once it has reached the end of its counter, it will take the updated list with the subtracted patients, and store them in a new CSV
#We then delete the existing CSV that was used originally, and rename the new CSV the same as the original CSV
#Then we break the loop to ensure its completed

mrn_list=[]  
i = 0
GivenName = 6 # Column that the Given Name resides in.  ***Future Enhancement - scan the list to find the location of Given Name and update the value in this variable
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


with open(loc_fn, mode='r') as csv_file:
     csv_reader = csv.reader(csv_file)
     for row in csv_reader:
         if i < len(asps): # if i is less than the number of images in the directory specified then do the below
             print(i)
             random_num=random.randint(1, lines) #We generate a random number between 1 and the number lines that we calculated the CSV to be
             #fake_patients = list(csv_reader)
             mrn_num = str(random.randrange(1, 10**7))
             num_with_zeros = str(mrn_num).zfill(3)
             mrn_list.append(mrn_num)
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
             print(value_GN,value_Sur)
             name = value_GN + " " + value_Sur #Concatonate the two values together to give us a firstname and lastname
             print(name)
             print(value_B_date)
             B_date_split=value_B_date.split("/")
             print(B_date_split)
             for z in range(0, len(B_date_split)):
                 B_date_split[z] = int(B_date_split[z])
             B_date_split = ["%02d" % n for n in B_date_split]
             date_order = [2, 0, 1]
             B_date_ordered = [B_date_split[t] for t in date_order]
             year = ''.join(str(e) for e in B_date_ordered)
             print(year)
             full_address = (value_Address + "^^" + value_City + "^" + value_State + "^" + value_Zip)
             dt=""
             r=datetime.datetime.now()
             dt=(r.strftime("%Y%m%d%H%M%S"))
             dt2=""
             q=datetime.datetime.now()
             dt2=(q.strftime("%Y%m%d%H%M%S"))
             cntrl_id = random.randrange(1, 10**6)
             # using format
             num_with_zeros = '{:03}'.format(cntrl_id)
             # using string's zfill
             num_with_zeros = str(cntrl_id).zfill(3)
             P_num_split=value_P_num.split("-")
             print(P_num_split)
             P_num_out = ''.join(p for p in P_num_split)
             print(P_num_out)
             os.chdir(loc_img_pth)
             basename="ADT_A01" #this csv we will dump the data in from our list - once we remove the top element from the list - creating a new list minus the patient we used
             milliseconds = int(round(time.time() * 1000))
             milli=str(milliseconds)[-3:]
             suffix=datetime.datetime.now().strftime("%S")
             temp_adt= ("_".join([basename, suffix]) + milli + '.txt')
             print(temp_adt)
             new_adt= open(temp_adt, mode='w')
             new_adt.write('MSH|^~\&|AccMgr|1|||%s||ADT^A01|%d|P|2.4||EVN|A01|%s|||||PID|1||%s||%s||%s|%s|1|%s|%s||1|2|||||||||||||||||||||||||||||||||||PV1|1|I|' % (dt, cntrl_id, dt2, mrn_num, name, year, value_Gender, full_address, P_num_out))
             new_adt.close()
             edit_it=(asps[i]) # We stored the location of the images above in a list.  This simply pulls the image from the list correspinding to its value - which is based on our counter = i.  for every trip through the loop - i will goup by one, which will then pull the next image in the list.
             name_go = '(0010,0010)={}'.format(name) # This was required to turn the name value into a string which is recognized by the command line subprocess call
             mrn_go = '(0010,0020)={}'.format(mrn_num)
             i += 1 # counter
             print(i)
             print("Finished ADT Stuff")
             os.chdir(dcmtk_loc_split)
             subprocess.check_call(["dcmodify", "-gst", "-ma", name_go, "-ma", mrn_go, edit_it],shell=True) #subprocess call which calls the dcmmodify.exe program to start the modification and feeds it the parameters including the patient name
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
                         




###########Generate random 6 digit number for Message Control ID
import random
cntrl_id = random.randrange(1, 10**6)
# using format
num_with_zeros = '{:03}'.format(cntrl_id)
# using string's zfill
num_with_zeros = str(cntrl_id).zfill(3)
print(cntrl_id)