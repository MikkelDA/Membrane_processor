def membrane_calculator(Norm_targets, requested, lipid_target = False):
    '''



    lipid_target: Must be an integer. Lipids will be normalized towards this number.
    Note that the sum of lipids may not be exactly equal to lipid_target due to rounding.
    The percentage makeup of lipids is also given.
    '''
    
    if lipid_target != False:
        if type(lipid_target) == str:
            assert isdigit(lipid_target), "lipid_target must be an integer"
            lipid_target = int(lipid_target)
    memb_comp = {}
    memb_sub_comp = {}
    assert type(requested) == list or requested == "all", "Requested must be either a list or 'all'"
    
    ### If "all" then create Requested list containing all fully named lipids from Norm_targets
    if requested == "all":
        Requested = [
            key for key in Norm_targets.keys()
            if key not in [key2[:len(key)] for key2 in Norm_targets.keys() if key != key2]
        ]
    else:
        Requested = requested[:]


    for lipid in Requested:
        memb_comp[lipid] = {}
        memb_comp[lipid]["comp"] = 1
    norms = {}
    Requested_subsets = {}
    for key in Requested:
        ### List of all subsets of "key" including all tuple indexes to the left of "i"
        key_subsets_list = [key[:i] for i in range(1, len(key) + 1)]
        for key_int, key_subset in enumerate(key_subsets_list, 1):
            ### Checks if subset already calculated. No need to do it twice
            if key_subset not in Requested_subsets.keys():
                ### Subsets to be summed over for subset of lipid definition normalization factor
                Requested_subsets[key_subset] = set([
                    req_key[:key_int] for req_key in Requested
                    if key_int == 1
                    or key_subset[:key_int - 1] == req_key[:key_int - 1]])

                ### Finding normalization factor for subset of lipid definition
                memb_sub_comp[key_subset] = {}
                memb_sub_comp[key_subset]["Norm_factor"] = pow(sum([Norm_targets[req_subset]
                                                                    for req_subset
                                                                    in Requested_subsets[key_subset]]), -1)

            ### Normalizing lipid with normalization factor for subset of lipid definition
            memb_comp[key]["comp"] *= memb_sub_comp[key_subset]["Norm_factor"] * Norm_targets[key_subset]


    ### ### Normalizing membrane towards 100%
    for key in memb_comp.keys():
        memb_comp[key]["percent"] = memb_comp[key]["comp"] * 100
    ### ### Normalizing membrane towards "lipid_target" lipids
    if lipid_target != False:
        for lipid in memb_comp.keys():
            memb_comp[lipid]["lipids"] = round(memb_comp[lipid]["comp"] * lipid_target)
        lipid_percent_norm = pow(sum([memb_comp[lipid]["lipids"] for lipid in memb_comp.keys()]), -1)
        for lipid in memb_comp.keys():
            memb_comp[lipid]["lipids_percent"] = lipid_percent_norm * memb_comp[lipid]["lipids"] * 100

    ### ### Creating dictionary of compositions and lipid compositions for all subsets
    for req_subset in Requested_subsets.keys():
        req_subset_sum = 0
        req_subset_len = len(req_subset)
        for subset in memb_comp.keys():
            if req_subset == subset[:req_subset_len]:
                req_subset_sum += memb_comp[subset]["comp"]
        memb_sub_comp[req_subset] = {}
        memb_sub_comp[req_subset]["comp"] = req_subset_sum
        memb_sub_comp[req_subset]["percent"] = memb_sub_comp[req_subset]["comp"] * 100
        if lipid_target != False:
            memb_sub_comp[req_subset]["lipids"] = round(req_subset_sum * lipid_target)
            memb_sub_comp[req_subset]["lipids_percent"] = lipid_percent_norm * memb_sub_comp[req_subset]["lipids"] * 100
    
    output = {
            "memb_comp": memb_comp,
            "memb_sub_comp": memb_sub_comp,
            }
    
    return output

