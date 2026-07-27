import os
import datetime


def create_log_directory():

    # ------------------------------------------------------------------
    # Create the log directory if it does not already exist.
    # ------------------------------------------------------------------

    if os.path.isdir("DiskSanitizer_Log"):
        return

    os.mkdir("DiskSanitizer_Log")


def create_log_file():

    # ------------------------------------------------------------------
    # Generate a unique log file name using the current timestamp.
    # ------------------------------------------------------------------

    timestamp = datetime.datetime.now()
    timestamp = timestamp.strftime("%d_%m_%Y_%H_%M_%S")

    log_file_name = f"DuplicateFileLog_{timestamp}.log"
    log_file_path = os.path.join("DiskSanitizer_Log", log_file_name)

    with open(log_file_path, "w"):
        pass

    return log_file_path


def write_log(log_path, message):

    # ------------------------------------------------------------------
    # Append the given message to the log file.
    # ------------------------------------------------------------------

    with open(log_path, "a") as log_file:
        log_file.write(str(message) + "\n")