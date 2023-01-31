import re

def norm_file_reader(norm_file):
    '''
    Imports a file containing normalization targets
        Guide on writing an input file containing normalization parameters:
            The file can contain empty lines and comments using '#'. Parameters contain
            two parts (key and value) and a separator (:) resulting in key:value. Note t
            hat the rightmost ':' on a line is used as separator, meaning that a key can
            contain ':'.
        Key:
            Each key must follow a logical 'left-to-right' order of indexing where each
            index to the left of a given index must be separately defined with a ratio v
            alue. Indexes in keys are separated by a comma ','.
            Keys can contain 'all' which results in this key being created for all keys
            with the same prior key indexes (to the left of 'all').
            Keys can also contain parenthesis (specifically round parenthesis '(elements
            )'), which forces the key to be generated for each element within the parent
            hesis separately.
            See the examples below for a demonstration.
        Ratio:
            The ratio value can be represented either as a number (integer or float) (su
            ch as 5 or 7.6) or as a mix of summations and/or subtractions (ex: 37.7 + 4.
            9 + 3.4 - 17.9). Note that the the values are RATIOS and not PERCENTAGES, me
            aning that they do not need to equal any specific number. The ratio for the
            lipids chosen to make a membrane are normalized both partway through the cal
            culations and at the end towards 100%.
        Example:
            PL: 46.8
            ST: 37.7 + 4.9 + 3.4
            PL,Outer: 35
            PL,Inner: 65
            ST,Outer: 70
            ST,Inner: 30
            PL,all,PC: 35.5 # Creates: 'PL,Outer,PC: 35.5' and 'PL,Inner,PC: 35.5'
            PL,all,PE: 5.5
            PL,all,PG: 9.0
            PL,all,PC,18:0:18:0: 18.7
            PL,all,PE,18:0:18:0: 16.3
            PL,all,PG,18:0:18:0: 9.1
            PL,all,(PC,PG),18:0:18:1: 19.3
            # Above creates 'PL,all,PC,18:0:18:1: 19.3', 'PL,all,PG,18:0:18:1: 19.3'
            PL,all,PE,18:0:18:1: 17.3
            ST,all,FS: 37.7
    '''
    def simple_calculator(string): ### Calculator to handle ratio number in case plus and/or minus is present
        numbers = []
        number = ""
        signs = []
        for i in string:
            if i.isdigit() or i == ".":
                number += i
            elif any([i == op for op in ["+", "-"]]):
                signs.append(i)
                numbers.append(number)
                number = ""
        numbers.append(number)
        res = float(numbers[0])
        if len(numbers) != 1:
            for i_nr, i in enumerate(numbers[1:]):
                if signs[i_nr] == "+":
                    res += float(i)
                elif signs[i_nr] == "-":
                    res -= float(i)
        return res
    
    Norm_targets = {}
    alls = []
    multiples = []
    with open(norm_file, "r") as f:
        for line_nr, line in enumerate(f):
            if line[0] == "#":
                continue
            elif "#" in line:
                line = line.split("#")[0]
            if ":" in line:
                for i in ["\n", "[", "]", ";"]:
                    line = line.replace(i, "")
                ### Splits from the right to allow for ':' in keys
                key, ratio = line.rsplit(":", maxsplit = 1)
                ### Used to identify multiples '(PC, PG, PA) etc.'
                keys = list(filter(lambda x:x!=None and x!="", re.split("\((.*?)\)|,", key.replace(" ", ""))))
                if "all" in keys:
                    alls.append([tuple(keys), simple_calculator(ratio)])
                elif any(["," in key for key in keys]):
                    multiples.append((tuple(keys), simple_calculator(ratio)))
                else:
                    if tuple(keys) not in Norm_targets.keys():
                        Norm_targets[tuple(keys)] = simple_calculator(ratio)
    
    #### Below handles alls. example: 'PL,all,PC,18:0:18:0: 50' 
    while len(alls) != 0:
        new_alls = []
        for (key, ratio) in alls:
            all_index = key.index("all")
            ref_keys = [ref_key for ref_key in Norm_targets.keys()
                        if len(ref_key) == all_index + 1
                        and key[:all_index] == ref_key[:-1]]
            for ref_key in ref_keys:
                new_key = tuple(ref_key + key[all_index + 1:])
                if "all" in new_key:
                    new_alls.append((new_key, ratio))
                elif any(["," in key for key in new_key]):
                    multiples.append((new_key, ratio))
                else:
                    if new_key not in Norm_targets.keys():
                        Norm_targets[new_key] = ratio
        alls = new_alls

    ### Below handles multiples. example: 'PL,Outer,(PC, PG, PA),18:0:18:0: 50'
    while len(multiples) != 0:
        new_multiples = []
        for (key, ratio) in multiples:
            mult_index = [idx for idx, sub_key in enumerate(key) if ',' in sub_key][0]
            mult_sub_keys = key[mult_index].split(",")
            for mult_sub_key in mult_sub_keys:
                if any(["," in key for key in new_key]):
                    new_multiples.append((tuple(key[:mult_index] + (mult_sub_key,) + key[mult_index + 1:]), ratio))
                else:
                    Norm_targets[tuple(key[:mult_index] + (mult_sub_key,) + key[mult_index + 1:])] = ratio
        multiples = new_multiples
    return Norm_targets

def norm_changer(Norm_targets, requested_changes):
    '''
    Changes normalization ratio value for single lipid.
    Example:
    'PL,Outer:50' changes 'PL,Outer' from the original value (eg. 65) to 50
    '''
    for request in requested_changes:
        lipid, value = request.split(":")
        key = tuple(lipid.split(","))
        Norm_targets[key] = int(value)
    return Norm_targets








