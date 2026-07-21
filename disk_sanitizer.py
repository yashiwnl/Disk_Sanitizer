"""
Disk Sanitizer

Deletes:
• Empty files
• Duplicate files

Uses:
• Recursive directory traversal
• MD5 checksum
• Size-based optimization

Author: Yash Sachin Satarkar
"""

#############################################################################################
#
#     Importing required Libraries 
#
#############################################################################################

import sys
import os
import time
import hashlib

#############################################################################################
#
#     Function name: empty_files_scanner
#     Input: Name of Directory
#     Description: Deletes all empty files periodically 
#     Date: 21/07/2026
#     Author: Yash Sachin Satarkar
#
#############################################################################################

def empty_files_scanner(directory_path):
  border = "-"*40
  timestamp = time.ctime
  log_file_name = "Empty_File %s.log"%timestamp()
  log_file_name = log_file_name.replace(" ", "_")
  log_file_name = log_file_name.replace(":", "_")
   

  if not os.path.exists(directory_path):
    print("Disk Sanitizer Error: There is no such directory with name: ",directory_path)
    return
  
  

  if not os.path.isdir(directory_path):
    print("Disk Sanitizer error: It is not a directory with name: ",directory_path)
    return

  with open(log_file_name, "w") as lfobj:

    lfobj.write(border + "\n")
    lfobj.write("Disk Sanitizer Script \n")
    lfobj.write(border + "\n\n")

    lfobj.write("Files from the directory are: \n\n")
    lfobj.write(border + "\n")

    total_files = 0
    empty_files = 0

    for folder_name, sub_folder, file_name in os.walk(directory_path):
        
      for fname in file_name:
        total_files += 1
        fname = os.path.join(folder_name,fname)

        lfobj.write(fname + ":" + str(os.path.getsize(fname)) + "bytes" + "\n")

        if os.path.getsize(fname) == 0:
          try: 
            os.remove(fname)
            empty_files += 1
            print("Empty file deleted: ", fname)         
          except Exception as e:
            print(f"Unable to delete {fname} : {e} ")

    lfobj.write(border + "\n")
    lfobj.write("Total files scanned: "+str(total_files)+"\n")
    lfobj.write("total empty files found and deleted: "+str(empty_files)+"\n")
    lfobj.write(border + "\n")


#############################################################################################
#
#     Function name: calculate_checksum
#     Input: name of the file of which you want to calculate checksum
#     Description: inputs file,  calcuates checksum and returns it
#     Date: 21/07/2026
#     Author: Yash Sachin Satarkar
#
#############################################################################################

def calculate_checksum(filename):
  
  with open(filename, "rb") as file:

    hobj = hashlib.md5()

    buffer = file.read(4096)

    while len(buffer) > 0:
      hobj.update(buffer)
      buffer = file.read(4096)

    return hobj.hexdigest()

#############################################################################################
#
#     Function name: duplicate_files_scanner
#     Input: Name of Directory
#     Description: Deletes all duplicate files periodically 
#     Date: 21/07/2026
#     Author: Yash Sachin Satarkar
#
#############################################################################################

def duplicate_files_scanner(directory_path):
  border = "-"*40
  timestamp = time.ctime
  log_file_name = "Duplicate_File %s.log"%timestamp()
  log_file_name = log_file_name.replace(" ", "_")
  log_file_name = log_file_name.replace(":", "_")
   

  if not os.path.exists(directory_path):
    print("Disk Sanitizer Error: There is no such directory with name: ",directory_path)
    return

  if not os.path.isdir(directory_path):
    print("Disk Sanitizer error: It is not a directory with name: ",directory_path)
    return

  with open(log_file_name, "a") as lfobj:

    total_files = 0
    duplicate_files = 0
    size_dict = {}
    for folder_name, sub_folder, file_name in os.walk(directory_path):
        
      for fname in file_name:
        total_files += 1

        fname = os.path.join(folder_name,fname)
        fsize = os.path.getsize(fname)
        if fsize not in size_dict:
        
          size_dict[fsize] = [fname]
        else:
          size_dict[fsize].append(fname)

    
    for size in size_dict:

      if len(size_dict[size]) > 1:
        checksum_dict = {}

        for filename in size_dict[size]:
          
          try:
            checksum = calculate_checksum(filename)
          except Exception as e:
            print(f"Unable to calculate checksum for {filename} : {e} ")
            continue

          if checksum not in checksum_dict:
            checksum_dict[checksum] = filename
          else:
            try:
              os.remove(filename)
              print("Duplicate file deleted:", filename)
              duplicate_files += 1
            except Exception as e:
              print(f"Failed to delete duplicate file: {filename} : {e}  ")



    lfobj.write("\n" +border + "\n")
    lfobj.write("Total files scanned: " + str(total_files) + "\n")
    lfobj.write("Total duplicate files found and deleted: "+str(duplicate_files)+"\n")
    lfobj.write(border + "\n")




#############################################################################################
#
#     Function name: main
#     Input: Command line Arguments
#     Description: It controls the script 
#     Date: 21/07/2026
#     Author: Yash Sachin Satarkar
#
#############################################################################################

def main():

  border = "-"*40
  print(border)
  print("Disk Sanitizer Script")
  print(border)

  if len(sys.argv) == 2:
    if sys.argv[1] == "--h" or sys.argv[1] == "--H":
       print("This automation script is used to scan the directory and delete empty or duplicate files ")
       print("For better usage please check --u flag")

    elif sys.argv[1] == "--u" or sys.argv[1] == "--U":
       print("Please execute the script as: ")
       print("python file_name.py directory_name")
       print("Directory name should be absolute path")

    else:
      empty_files_scanner(sys.argv[1])
      duplicate_files_scanner(sys.argv[1])
  else:
    print("invalid no of arguments only two are required")
    print("please use --h or --u for more information")
  
  print(border)
  print(" Thank You for using Disk Sanitizer")
  print(border)


#############################################################################################
#
#     Starter of Automation Script 
#
#############################################################################################

if __name__ == "__main__":
    main()