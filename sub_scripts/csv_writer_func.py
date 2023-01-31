### import backup function 
from .backupper_func import *
import csv

def csv_dict_writer(dictionary, write_lipids = False, headers = None, decimals = 3, lipid_target = None, file_path = None, return_csv = False, backup = True):
    '''
    dictionary: Dictionary with calculated membrane parameters

    headers:
        Must be lists of two tuples (selectors and heads).
        Selector:
        The selector can consist of any number of tuples/lists (all indexes must be tuples/lists).
        The tuples/lists in the selector contain subkeys that will define what keys in the
        dictionary will be mapped to the heads. The subkeys do not need to be present
        in the key in the same order as they are listed in the key, but all must be
        present in the key.
        Heads:
        The heads must contain strings. These will be used as headers in the csv file.
        Example:
        headers = [
            ### 'PL' as selector ('PL' must be in key)
            ((("PL",),),
             ("Lipid_type", "Leaf", "Headgroup/Core", "Tail")),
             
            ### 'CER' as selector ('CER' must be in key)
            ((("CER",),),
             ("Lipid_type", "Leaf", "Headgroup/Core", "Tail")),
             
            ### Both 'ST' and 'FS' in key or both 'ST' and 'SG' in key
            ((("ST","FS",), ("ST","SG",),),
             ("Lipid_type", "Leaf", "Sterol glycosylation", "Headgroup/Core")),
             
            ### Both 'ST' and 'FS' in key
            ((("ST","ASG",),),
             ("Lipid_type", "Leaf", "Sterol glycosylation", "Headgroup/Core", "Tail")),
        ]
        If no header is supplied then one will be generated using the subkey index as header.
    
    decimals: Number of decimals printed (default = 3)
    
    file_path: File path and name for the csv file.
    If no 'file_path' is given then the csv file will be returned

    '''
    ### Generates headers if no headers given
    if headers == None:
        number_of_headers = max(len(key) for key in dictionary.keys())
        heads = ["Subkey_" + str(nr) for nr in range(1, number_of_headers + 1)]
        seps = list(set([key[0] for key in dictionary.keys()]))
        headers = [(((sep,),), tuple(heads)) for sep in seps]
    ### Ensures that all headers have both a selector and a head
    else:
        for nr, head in enumerate(headers):
            assert len(head) == 2 and all([any([type(head[i]) == t for t in [tuple, list] for i in [0, 1]])]), "Each header must have at least one separator tuple and one head list defined"
            assert any([type(head[0]) == t for t in [tuple, list]]), "Separators must be tuples or lists"
            assert any([type(head[1]) == t for t in [tuple, list]]), "Head must be tuple or list"
            
    headers_formatted = []
    data = []
    selectors = {}
    ### Loop over each header tuple
    for sels, heads in headers:
        for i in heads:
            ### Makes list of all possible headers. Ensures no duplicate headers
            if i not in headers_formatted:
                headers_formatted.append(i)
        ### Registers the heads for each selector given
        for sel in sels:
            selectors[sel] = heads
    
    dict_sorted = sorted(dictionary.keys(), key=lambda x: x, reverse = False)
    ### 
    lacking_selector_header_combo = False
    for key in dict_sorted:
        data_line = []
        zipped = []
        ### Creates list of (subkey, header) tuples
        for sel in selectors.keys():
            if all(any([s == subkey for subkey in key]) for s in sel):
                if len(key) > len(selectors[sel]):
                    print("WARNING: Number of key indexes is greater than the number of selector indexes")
                    print("    ", "Key and key length:", key, len(key))
                    print("    ", "Selector and selector length:", selectors[sel], len(selectors[sel]), end="\n\n")
                zipped = list(zip(key, selectors[sel][:len(key) + 1]))
                
        
        ### Checks if selector found for key. Prints warning and continues to next key if not
        if zipped == []:
            print("WARNING: No selector:header combo found for key:", key)
            lacking_selector_header_combo = True
            continue
        
        ### Appends data for key to correct header indexes
        for header in headers_formatted:
            ### Finds subkey, head combo
            for (subkey, subheader) in zipped:
                if header == subheader:
                    data_line.append(subkey)
                    break
            ### If combo found, add empty string
            else:
                data_line.append("")
        
        ### Data from membrane calculations
        data_line.append(round(dictionary[key]["percent"], decimals))
        ### Lipid specific calculations
        if write_lipids == True:
            #lipid_check = all(["lipids" in dictionary[key].keys() for key in dictionary.keys()])
            lipid_check = "lipids" in dictionary[key].keys()
            assert lipid_check == True, "Lipids requested, but none calculated for dictionary"
            data_line.append(dictionary[key]["lipids"])
            data_line.append(round(dictionary[key]["lipids_percent"], decimals))
        ### Append to total data list if it is not already there (in case of duplicate entries)
        if data_line not in data:
            data.append(data_line)            
    
    ### If Warning printed earlier about no selector:header combo then print this for debugging purpose
    if lacking_selector_header_combo == True:
        print("Selectors used:", *selectors.keys(), end="\n\n")
    
    ### Add headers for membrane calculations
    headers_formatted.append("Percentage of membrane (%)")
    if write_lipids == True:
        lipid_check = all(["lipids" in dictionary[key].keys() for key in dictionary.keys()])
        assert lipid_check == True, "Lipids requested, but none calculated for dictionary"
        lipid_sum = sum([dictionary[key]["lipids"] for key in dictionary.keys()])
        ### Writes lipid target if supplied. Otherwise writes only lipid sum
        if lipid_target != None:
            headers_formatted.append("Lipids (Target: " + str(lipid_target) + ", " + "Total: " + str(lipid_sum) + ")")
        else: headers_formatted.append("Lipids (Total: " + str(lipid_sum) + ")")
        headers_formatted.append("Lipid percentage of membrane (%)")
    
    ### Writes csv file
    if file_path != None:
        ### Backup already existing file with same name
        if backup != False:
            backupper(file_path)
        else:
            print("Backup not requested. Will overwrite file if it already exists.")
        with open(file_path, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(headers_formatted)
            for row in data:
                writer.writerow(row)
    if return_csv != False:
        return [headers_formatted] + data


