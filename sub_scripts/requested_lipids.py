import re
import itertools
import ast

def load_lipid_files(*args, input_list = None):
    '''
    *args (lipid_files): Path to files containing lipid request data
    Multiple files can be given
    Returns a list of lipids to be used with 'lipid_processer'
    
    input_list: Adds lipid request data to an existing list instead of creating a new one
    
    Outputs a dictionary containing:
    "requested_lipids": the requested lipids
    "lipid_target": the requested lipid target
    "csv_header": header to be used with csv_writer

    '''
    lipid_files = args
    ### Creates empty list for return
    if input_list == None:
        requested_lipids = []
    ### Adds requests to supplied list
    else:
        assert type(input_list) == list, "input_list given, but it is not a list"
        requested_lipids = input_list
    
    lipid_target = False
    csv_header = None
    for lipid_file in lipid_files:
        with open(lipid_file, "r") as f:
            for line_nr, line in enumerate(f):
                ### ### ### ### Preprocess line for readability and comments
                ### Ignore line if "#" as first index (ignore comment)
                if line[0] == "#":
                    continue
                ### Only use what is to the left of a "#" (ignore comment)
                elif "#" in line:
                    line = line.split("#")[0]
                ### Removes newlines
                for i in ["\n"]:
                    line = line.replace(i, "")

                ### ### ### ### Data type checks and processing
                ### Checks if line designates a lipid target
                if line.startswith("lipid_target"):
                    lipid_target = int(line.replace("\n", "").replace(" ", "").split("=")[-1])
                    continue
                ### Checks if line designates headers for csv writing
                elif line.startswith("csv_header"):
                    csv_header = ast.literal_eval(line.replace(" ", "").split("=")[-1])
                    continue
                ### If line not empty process line as if lipid request
                elif line.strip() != "":
                    requested_lipids.append(line)
    output = {
            "requested_lipids": requested_lipids,
            "lipid_target": lipid_target,
            "csv_header": csv_header,
            }

    return output

def lipid_request_processer(*args, Requested_lipids = False, Norm_targets = None):
    '''
    *args (list of requested_lipids): List of list(s) of requested lipids.
    
    Requested_lipids: Existing list to which *args will be added.
    If no list given, then an empty one will be used

    Norm_targets: Dictionary of normalization targets
    Examples:
    'PL,Outer,PC,16:0:18:2' - Normal request with no subcommands
    'PL,Outer,PC,16:0:18:2-SR:500' - Ratio scaled by 500% (returned in ratio_changes)
    'PL,Inner,PC,16:0:18:2-SR:500' - 'Inner' instead of 'Outer'
    The two commands above can be given as separate flags:
    'PL,Outer,PC,16:0:18:2-SR:500 -L PL,Inner,PC,16:0:18:2-SR:500'
    or combined into one flag:
    'PL,(Outer,Inner),PC,16:0:18:2-SR:500'
    
    Subcommand explanation:
    SR:Percentage - Scales the lipid normalization target by 'Percentage' (integer or float)

    Returns the following tuple if no Norm_targets is supplied:
    (list of lipid requests for 'membrane_calculator', dictionary of scalings for 'norm_scaler')
    eg: (Requested, ratio_changes)

    Alternatively:
    Returns the following tuple if Norm_targets is supplied:
    (list of lipid requests for 'membrane_calculator', modified Norm_targets based on ratio scalings)
    eg: (Requested, new_Norm_targets)
    '''
    ratio_changes = {} # Dict of ratio changes for Norm_targets
    request_lists = args
    if Requested_lipids == False:
        Requested = []
    else:
        Requested = Requested_lipids
    ### Loops over the requests
    for requested_lipids in request_lists: 
        for request in requested_lipids:
            ### Loops of the parts of the request
            for nr, part in enumerate(request.split("-")):
                ### First part always has to be the key:value definition 
                if nr == 0:
                    part = "".join(part.replace(" ", ""))
                    ### If multiple strings given for the same index. Eg. 'PL,(Outer,Inner),PC'
                    if "(" in part:
                        part_split = list(filter(lambda x:x!=None and x!="", re.split("\((.*?)\)|,", part)))
                        while "" in part_split:
                            part_split.remove("")
                        for nr, i in enumerate(part_split):
                            part_split[nr] = list(filter(lambda x:x!="", i.split(",")))
                        lipids = list(itertools.product(*part_split))
                    ### If no multiples
                    else:
                        lipids = [part.split(",")]
                ### Process subcommands for request
                else:
                    command, settings = part.split(":", maxsplit = 1)
                    ### Scale ratio by given percentage
                    if command == "SR":
                        for lipid in lipids:
                            ratio_changes[tuple(lipid)] = int(settings) / 100
            for lipid in lipids:
                Requested.append(tuple(lipid))
    
    if len(ratio_changes.keys()) != 0:
        Norm_targets = norm_scaler(Norm_targets, ratio_changes)

    output = {
            "Requested": Requested,
            "ratio_changes": ratio_changes,
            "Norm_targets": Norm_targets
            }

    return output

#    if Norm_targets == None:
#        return (Requested, ratio_changes)
#    else:
#        new_Norm_targets = norm_scaler(Norm_targets, ratio_changes)
#        return (Requested, new_Norm_targets)

def norm_scaler(Norm_targets, ratio_changes):
    '''
    Norm_targets: Dictionary of normalization targets
    ratio_changes: Dictionary of requested scalings
    
    Function: Scales normalization targets in 'Norm_targets' by scalings requested in 'ratio_changes'
    
    Returns
    Modified Norm_targets
    '''
    for key in ratio_changes.keys():
        for target_key in Norm_targets.keys():
            if key == target_key:
                Norm_targets[key] *= ratio_changes[key]
    return Norm_targets

