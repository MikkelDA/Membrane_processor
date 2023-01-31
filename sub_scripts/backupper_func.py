import sys
import os.path
### Checks if output file already exists and backs it up
def backupper(output_file_name):
    output_file_split = output_file_name.split("/")
    output_path = ""
    output_name = output_file_split[-1]
    if len(output_file_split) > 1:
        for i in range(len(output_file_split) - 1):
            output_path += output_file_split[i] + "/"
    if os.path.exists(output_file_name):
        print("File " + output_file_name + " already exists. Backing it up")
        number = 1
        while True:
            if os.path.exists(output_path + "#" + output_name + "." + str(number) + "#"):
                number += 1
            else:
                os.rename(output_file_name, output_path + "#" + output_name + "." + str(number) + "#")
                break
