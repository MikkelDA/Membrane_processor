import math

def insane_converter(
    ### Lipid commands
    memb_dict: dict, # "comp_memb" dictionary
    insane_translator_list: list, # "memb_comp" to "insane lipid name" translator
    leaf_placement_list: list or False = False, # Specifies which key(s) in insane_translator_dict dictates leaf
    leafs: str = "both", # ("both", "b"), ("lower", "l", "inner", "i"), ("upper", "u", "outer", "o")
    ### strings within tuples will be treated identically
    return_only_lipids: bool = False, # Returns a list consisting only of lipid names

    ### Asymmetry commands
    return_asymmetry: bool = False, # Returned string contains the asymmetry commands
    asymmetry_from_lipids: bool = False, # Calculate asymmetry from lipids
    leaflet_to_scale = "lower", # Specifies which leaflet will be scaled from
    leaflet_scaling_ratio: float or int = 1, # Ratio used to scale the "leaflet_to_scale"
    apl_lower: float = 0.6, # Has its square root taken in INSANE. Default 0.6
    apl_upper: float = 0.6, # Has its square root taken in INSANE for py3 and my modified script
    ### ### apl_upper Does not have its square root taken in INSANE py2 from Kasper
    fit_box_to_asym: bool = False, # fits x, y and/or d to apl_lower and apl_upper
#     asym_fit_func: max or min = max,
    box: list = None,
    d: float or False = False,
):
    ### Preprocess "leafs"
    leafs = leafs.lower()
    if leafs in ("both", "b"):
        leafs = "both"
    elif leafs in ("lower", "l", "inner", "i"):
        leafs = "lower"
    elif leafs in ("upper", "u", "outer", "o"):
        leafs = "upper"
    else:
        assert False, "Unapplicable 'leafs' command given"
    
    leaflet_to_scale = leaflet_to_scale.lower()
    if leaflet_to_scale in ("lower", "l", "inner", "i"):
        leaflet_to_scale = "lower"
    elif leaflet_to_scale in ("upper", "u", "outer", "o"):
        leaflet_to_scale = "upper"
    else:
        assert False, "Unapplicable 'leaflet_to_scale' command given"
    
    if box:
        x, y, z = box

    ### Function to check find key:translator match
    def key_index_checker(key, translator_list):
        for (indexes, subkeys, name) in translator_list:
            ### Checks if each designated index in key matches the required subkey for "name"
            key_checker = 0
            if len(key) >= max(indexes) + 1:
                for (index, subkey) in zip(indexes, subkeys):
                    if key[index] == subkey:
                        key_checker += 1

            ### Appends insane lipid name and ends iteration over the translator list
            if key_checker == len(indexes):
                return name
    
    insane_command = []
    ### Creates all commands for insane
    lipid_commands = []
    l_count = 0
    u_count = 0
    for key in memb_dict.keys():
        key_command = []
        
        ### ### Leaflet designation
        if leaf_placement_list != False:
            key_command.append(key_index_checker(key, leaf_placement_list))
        else:
            key_command.append("-l")
        
        ### Skips the lipid if it is not a part of the requested leaflet
        if ((leafs, key_command[0]) == ("lower", "-u")) or ((leafs, key_command[0]) == ("upper", "-l")):
            continue
        elif leafs == "upper": # Default lipid addition leaflet is "lower" in INSANE
            key_command[0] = "-l"
        
        ### Adding to asymmetry for leaflet
        if key_command[0] == "-l":
            l_count += memb_dict[key]["percent"]
        elif key_command[0] == "-u":
            u_count += memb_dict[key]["percent"]
        
        ### ### Lipid name translation
        key_command.append(key_index_checker(key, insane_translator_list))
        
        key_command.append(memb_dict[key]["percent"])
        
        lipid_commands.append(key_command)

    lipid_commands = sorted(lipid_commands, key=lambda x: (x[0], x[1], x[2]), reverse = True)
    
    if return_only_lipids:
        return [lipid for command, lipid, val in lipid_commands]

    ### Joining all the commands together into one string
    insane_command_string = " ".join([
        " ".join([leaf, ":".join([lipid, str(round(val, 2))])])
        for leaf, lipid, val in lipid_commands
    ])
    
    if return_asymmetry == True:
        ### Creating asymmetry commands for INSANE (flags "-a" and "-au")
        if leaflet_to_scale == "upper":
            if asymmetry_from_lipids == True:
                apl_upper /= u_count / l_count
            apl_upper /= leaflet_scaling_ratio
        elif leaflet_to_scale == "lower":
            if asymmetry_from_lipids == True:
                apl_lower *=  u_count / l_count
            apl_lower *= leaflet_scaling_ratio
        insane_command_string = " ".join([insane_command_string, " ".join(["-a", str(round(apl_lower, 3))])])
        insane_command_string = " ".join([insane_command_string, " ".join(["-au", str(round(apl_upper, 3))])])
    
    ### Adds an extra (0.01 * min(apl_lower, apl_upper)) to ensure rounding does not underestimate planar dimensions
    if box:
        ### Box dimensions ### x, y, z
        for variable, variable_name in zip([x, y, z], ["x", "y", "z"]):
            ### Fits given planar dimensions (x/y) to apl asymmetry
            if fit_box_to_asym:
                if variable_name == "x":
                    variable = max(variable // apl_lower * apl_lower, variable // apl_upper * apl_upper) + (0.01 * min(apl_lower, apl_upper))
                elif variable_name == "y":
                    variable = min(variable // apl_lower * apl_lower, variable // apl_upper * apl_upper) + (0.01 * min(apl_lower, apl_upper))
            insane_command_string = " ".join([insane_command_string, " ".join(["-" + variable_name, str(round(variable, 3))])])
    
    ### Box dimensions ### d
    elif not box and d:
        x = variable = max(d // apl_lower * apl_lower, d // apl_upper * apl_upper) + (0.01 * min(apl_lower, apl_upper))
        y = variable = min(d // apl_lower * apl_lower, d // apl_upper * apl_upper) + (0.01 * min(apl_lower, apl_upper))
        insane_command_string = " ".join([insane_command_string, " ".join(["-x", str(round(x, 3))])])
        insane_command_string = " ".join([insane_command_string, " ".join(["-y", str(round(y, 3))])])
        insane_command_string = " ".join([insane_command_string, " ".join(["-z", str(round(d, 3))])])
    
    return insane_command_string
