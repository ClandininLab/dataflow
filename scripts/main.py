import sys
import os
import warnings
import ftputil
import ftplib
import subprocess
from time import sleep
import dataflow as flow

warnings.filterwarnings("ignore",category=DeprecationWarning)
sys.stdout = flow.Logger()

target = 'F:/FTP_IMPORTS' # Where on this computer it goes
flag = '__flag__' #flag = '__flag__'
user = 'luke' # folder to look in E: drive in Bruker
ip='171.65.18.54'
username = 'user'
passwd = 'flyeye'
oak_target = 'X:/data/Brezovec/2P_Imaging/IMPORTS'
extensions_for_oak_transfer = ['.nii', '.csv', '.xml']
delete_source = False # Currently unused
convert_to = '.nii' # Currently unsused
quit_if_local_target_exists = True

##################################
### Transfer files from Bruker ###
##################################

# Connect via ftp
ftp_host = flow.connect_to_ftp(ip, username, passwd)

# Check if any folders have flag, QUIT IF NO
folder, metadata = flow.check_for_flag(ftp_host, flag)

# Set variables based on loaded metadata
oak_target = metadata['oak_target']
delete_source = metadata['delete_source']
convert_to = metadata['convert_to']

# Strip flag of folder and join to target
full_target = target + '/' + folder.replace(flag, '')

# Check if this folder exists, QUIT IF YES
flow.check_for_target(full_target, quit_if_local_target_exists) #checks if that flagless-folder already exists on target drive

# Send start email
flow.send_email(subject='Dataflow STARTED', message='Processing {}'.format(full_target))

# Copy from bruker computer to local computer
flow.start_copy_recursive_ftp(ftp_host, user + '/' + folder, full_target, ip, username, passwd)

#################################
### Convert from raw to tiffs ###
#################################

flow.convert_raw_to_tiff(full_target)

###########################
### Convert tiff to nii ###
###########################

flow.start_convert_tiff_collections(full_target)

#######################
### Transfer to Oak ###
#######################

flow.start_oak_transfer(full_target, oak_target, extensions_for_oak_transfer)

### Notify user via email ###
flow.send_email(subject='Dataflow COMPLETE',
				message='Processed {}\nProcessed files located at {}'.format(full_target, oak_target))

### Delete files from Bruker Computer ###