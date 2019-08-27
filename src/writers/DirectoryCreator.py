# Generate the Required Folder Structure
import os


def generate_folder_struct(path):
    try:
        os.makedirs(path)
    except OSError:
        print("Creation of the directory %s failed" % path)
    else:
        print("Successfully created the directory %s " % path)
