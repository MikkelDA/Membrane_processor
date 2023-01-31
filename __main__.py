'''
    If you want to run this program from the command line,
    then the command must involve the -m flag before the program.
    ex:
    python -m CPPM_calculator #Note that '.py' must not be included
    Flags should follow the above.
    ex:
    python -m CPPM_calculator -N normfile.txt
'''
import argparse
import sys
import ast

### Imports the package part
import __init__ as cppm


### ### ### ### ### ### ### ### Parser arguments begin ### ### ### ### ### ### ### ###

parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter,
                                 add_help = False)

### ### Parser for handling '-f' when importing module to Jupyter
#parser.add_argument("-f", dest = "debug_flag_for_jupyter")



### ### ### Help caller
parser.add_argument("-h", "--help", dest = "help")

### ### ### Normalization additions
parser.add_argument("-N", dest = "norm_file", default = False,
                    help = "Name of replacement normalization target file.\n"
                    "The file must be correctly formatted.\n"
                    "Default normalization parameters will be used if not supplied.\n")

### ### ### Normalization additions
# parser.add_argument("-o", dest = "output_name", default = False,
#                     help = "Output file containing membrane composition.")

# parser.add_argument("-oI", dest = "output_name_insane", default = False,
#                     help = "Output file in a format usable in for the Insane script.")

# parser.add_argument("-oL", dest = "output_name_latex", default = False,
#                     help = "Output file in a latex table format.")

parser.add_argument("-o_csv", dest = "output_name_csv", default = False,
                    help = "Output file in a csv format.")

#parser.add_argument("-o_csv_headers", dest = "output_name_csv_headers", default = None,
#                    help = "Headers for csv output file.")

parser.add_argument("-print_to_terminal", dest = "print_terminal", default = False,
                    help = "Print the membrane composition to terminal.")

#parser.add_argument("-log", dest = "log_name", default = False,
#                    help = "Name of output log file.\n"
#                    "A log file will not be created unless a name has been given.\n")

### ### ### Lipid-membrane stuff
#parser.add_argument("-L", dest = "requested_lipids", type=str, default = [], nargs='+',
#                    help = "Lipid to be added to membrane.\n")

parser.add_argument("-L_file", dest = "requested_lipids_files", type=str, default = [], nargs='+',
                    help = "File containing lipid to be added to membrane.\n")

#parser.add_argument("-LT", dest = "lipid_target", default = False,
#                    help = "Lipid target for membrane calculation.\n")

parser.add_argument("-C", dest = "absolute_changes", type=str, default = [], nargs='+',
                    help = "Changes normalization ratio value for single lipid.\n")

args = parser.parse_args()

### ### ### ### ### ### ### ### Parser arguments end ### ### ### ### ### ### ### ###


### Prints help and exits program
if args.help != None or len(sys.argv) == 1:
    cppm.print_helper()
    sys.exit()

### Checks all required files are present
assert args.norm_file != False, "A normalization file must be supplied with the '-N' flag"
assert args.requested_lipids != [] or args.requested_lipids_files != [], "At least one lipid request (for membrane creation) must be given. One of the flags '-L' or '-L_file' must be used at least once"

### Process normalization file and absolute normalization file scalings
Norm_file = args.norm_file
NormTargets = cppm.norm_file_reader(Norm_file)
if args.absolute_changes != []:
    absolute_changes = args.absolute_changes
    NormTargets = cppm.norm_scaler(absolute_changes, NormTargets)

### Process lipid requests
lip_req = args.requested_lipids
lip_req_files = args.requested_lipids_files

if lip_req_files != []:
    ### Outputs a dictionary
    lip_files_output = cppm.load_lipid_files(lip_req_files, lip_req)
    ### Retrieves dictionary values
    lip_req = lip_files_output["requested_lipids"]
    lipid_target = lip_files_output["lipid_target"]
    csv_headers = lip_files_output["csv_header"]

### Process requests and the scalings contained therein
norm_file_output = cppm.lipid_request_processer(lip_req, input_dict = Norm_file)
Requests, Norm_file = norm_file_output["Requested"], norm_file_output["Norm_targets"]

### Process lipid target
#if args.lipid_target != False:
#    lipid_target = args.lipid_target
#else:
#    lipid_target = False

memb, memb_sub = cppm.membrane_calculator(Norm_targets = Normtargets, Requested = Requests, lipid_target = lipid_target, data_return = "all")




### ### ### ### ### ### ### ### Outputs and prints ### ### ### ### ### ### ### ###
### Print to terminal
if args.print_terminal != False:
    print("Lipid composition")
    cppm.terminal_printer(memb_comp = memb, lipid_target = lipid_target, decimals = 3)
    print()
    print("Composition of all subdivisions")
    cppm.terminal_printer(memb_comp = memb_sub, lipid_target = lipid_target, decimals = 3)

### ### Write csv file:
### Header
#if args.output_name_csv_headers != None:
#    ### ast.literal_eval() is not dangerous like normal eval()
#    csv_headers = ast.literal_eval(args.output_name_csv_headers)
#else:
#    csv_headers = args.output_name_csv_headers # None by default
### Writing
if args.output_name_csv != False:
    output_name_csv = args.output_name_csv
    print("writing csv file")
    cppm.csv_dict_writer(
            dictionary = memb,
            write_lipids = lipid_target,
            headers = csv_headers,
            decimals = 3,
            lipid_target = lipid_target,
            file_path = output_name_csv,
            return_csv = False
            backup = True
            )








