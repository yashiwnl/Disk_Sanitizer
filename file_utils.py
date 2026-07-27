import os
import hashlib


def get_all_files(path):

# ------------------------------------------------------------------
# Recursively scans the directory and returns all file paths.
# ------------------------------------------------------------------

    file_list = []

    for folder_name, sub_folder, file_names in os.walk(path):

        for file_name in file_names:
            file_path = os.path.join(folder_name, file_name)
            file_list.append(file_path)

    return file_list




def calculate_checksum(file_path):

# ------------------------------------------------------------------
# Calculates and returns the MD5 checksum of a file.
# ------------------------------------------------------------------

    with open(file_path, "rb") as file_object:

        hash_object = hashlib.md5()

        buffer = file_object.read(4096)

        while len(buffer) > 0:
            hash_object.update(buffer)
            buffer = file_object.read(4096)

    return hash_object.hexdigest()




def find_duplicates(file_list):

# ------------------------------------------------------------------
# Finds duplicate files using MD5 checksum.
# ------------------------------------------------------------------

    checksum_dict = {}

    for file_path in file_list:

        checksum = calculate_checksum(file_path)

        if checksum in checksum_dict:
            checksum_dict[checksum].append(file_path)
        else:
            checksum_dict[checksum] = [file_path]

    return checksum_dict




def delete_duplicates(checksum_dict):

# ------------------------------------------------------------------
# Deletes duplicate files while keeping one original copy.
# ------------------------------------------------------------------

    duplicates = [
        files
        for files in checksum_dict.values()
        if len(files) > 1
    ]

    delete_count = 0
    deleted_files = []

    for files in duplicates:

        # Skip the first file and delete the remaining duplicates
        for file_path in files[1:]:

            try:
                os.remove(file_path)
                delete_count += 1
                deleted_files.append(file_path)

            except Exception:
                pass

    return delete_count, deleted_files