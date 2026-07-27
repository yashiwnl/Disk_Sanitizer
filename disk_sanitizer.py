import sys
import time
import schedule

import validator
import logger
import file_utils
import mail_sender

#############################################################################################
#
# Function Name : display_help
# Description   : Displays help information for the script.
#
#############################################################################################

def display_help():

    print("This script scans a directory, identifies duplicate files using checksums,")
    print("deletes duplicate files, creates a log file, and sends the log file through email.")
    print()
    print("Usage:")
    print("python duplicate_file_removal.py <AbsoluteDirectoryPath> <TimeIntervalInMinutes> <ReceiverEmailAddress>")
    print()
    print("Example:")
    print("python duplicate_file_removal.py /home/yash/Demo 30 abc@example.com")


#############################################################################################
#
# Function Name : display_usage
# Description   : Displays the correct command-line usage.
#
#############################################################################################

def display_usage():

    print("Usage:")
    print("python duplicate_file_removal.py <AbsoluteDirectoryPath> <TimeIntervalInMinutes> <ReceiverEmailAddress>")


#############################################################################################
#
# Function Name : perform_duplicate_removal
# Description   : Scans the directory, removes duplicate files,
#                 generates a log file and emails the report.
#
#############################################################################################

def perform_duplicate_removal(directory_path, receiver):

    border = "-" * 65

    # ------------------------------------------------------------------
    # Create Log File
    # ------------------------------------------------------------------

    logger.create_log_directory()
    log_path = logger.create_log_file()

    # ------------------------------------------------------------------
    # Scan Directory
    # ------------------------------------------------------------------

    start_time = time.ctime()

    try:

        file_list = file_utils.get_all_files(directory_path)

        checksum_dict = file_utils.find_duplicates(file_list)

        delete_count, deleted_files = file_utils.delete_duplicates(checksum_dict)

    except Exception as e:

        logger.write_log(log_path, f"Unexpected Error occurred : {e}")
        return

    end_time = time.ctime()

    # ------------------------------------------------------------------
    # Calculate Statistics
    # ------------------------------------------------------------------

    total_files = len(file_list)

    duplicate_count = 0

    for files in checksum_dict.values():

        if len(files) > 1:
            duplicate_count += len(files) - 1

    # ------------------------------------------------------------------
    # Write Log
    # ------------------------------------------------------------------

    logger.write_log(log_path, f"Log Generated At : {start_time}")
    logger.write_log(log_path, border)
    logger.write_log(log_path, "")
    logger.write_log(log_path, border)
    logger.write_log(log_path, "              Disk Sanitizer Script              ")
    logger.write_log(log_path, border)
    logger.write_log(log_path, "")

    logger.write_log(log_path, f"Directory Scanned : {directory_path}")
    logger.write_log(log_path, f"Receiver Email : {receiver}")
    logger.write_log(log_path, f"Scanning Started : {start_time}")
    logger.write_log(log_path, f"Scanning Completed : {end_time}")

    logger.write_log(log_path, border)

    logger.write_log(log_path, f"Total Files Scanned : {total_files}")
    logger.write_log(log_path, f"Duplicate Files Found : {duplicate_count}")
    logger.write_log(log_path, f"Duplicate Files Deleted : {delete_count}")

    logger.write_log(log_path, border)
    logger.write_log(log_path, "Duplicate Checksums")

    for checksum, files in checksum_dict.items():

        if len(files) > 1:

            logger.write_log(log_path, border)
            logger.write_log(log_path, f"Checksum : {checksum}")

            for file_path in files:
                logger.write_log(log_path, file_path)

    logger.write_log(log_path, border)
    logger.write_log(log_path, "Deleted Files :")

    for file_path in deleted_files:
        logger.write_log(log_path, file_path)

    logger.write_log(log_path, border)

    # ------------------------------------------------------------------
    # Prepare Email Body
    # ------------------------------------------------------------------

    body = f"""
Hello,

The duplicate-file removal operation has been completed successfully.

Operation Statistics

Starting time of scanning : {start_time}

Completion time of scanning : {end_time}

Directory scanned : {directory_path}

Total files scanned : {total_files}

Total duplicate files found : {duplicate_count}

Total duplicate files deleted : {delete_count}

Please find the detailed log file attached.

Regards,

Disk Sanitizer
"""

    # ------------------------------------------------------------------
    # Send Email
    # ------------------------------------------------------------------

    status = mail_sender.send_mail(receiver, log_path, body)

    if status:
        logger.write_log(log_path, "Email Status : SUCCESS")
    else:
        logger.write_log(log_path, "Email Status : FAILED")

    logger.write_log(log_path, border)


#############################################################################################
#
# Function Name : main
# Description   : Entry point of the application.
#
#############################################################################################

def main():

    border = "-" * 65

    print(border)
    print("              Disk Sanitizer Script")
    print(border)

    # ------------------------------------------------------------------
    # Display Help / Usage
    # ------------------------------------------------------------------

    if len(sys.argv) == 2:

        if sys.argv[1] in ("--h", "--help"):
            display_help()
            sys.exit()

        elif sys.argv[1] in ("--u", "--usage"):
            display_usage()
            sys.exit()

        else:
            print("Invalid option.")
            print("Use --help or --h for more information.")
            sys.exit()

    # ------------------------------------------------------------------
    # Validate Command-Line Arguments
    # ------------------------------------------------------------------

    if len(sys.argv) != 4:

        print("Invalid number of arguments.")
        print("Use --help for more information.")
        sys.exit()

    directory_path = sys.argv[1]
    interval = sys.argv[2]
    receiver = sys.argv[3]

    if not validator.validate_directory(directory_path):

        print("Invalid Directory")
        sys.exit()

    if not validator.validate_interval(interval):

        print("Invalid Time Interval")
        sys.exit()

    if not validator.validate_email(receiver):

        print("Invalid Email Address")
        sys.exit()

    # ------------------------------------------------------------------
    # Schedule Duplicate Removal
    # ------------------------------------------------------------------

    schedule.every(int(interval)).minutes.do(
        perform_duplicate_removal,
        directory_path,
        receiver
    )

    print("Script Started")
    print("Press Ctrl + C to Terminate Script")

    while True:

        schedule.run_pending()
        time.sleep(1)


#############################################################################################
#
# Starter of Automation Script
#
#############################################################################################

if __name__ == "__main__":
    main()