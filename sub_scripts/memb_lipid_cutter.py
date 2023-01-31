from .membrane_calculator import *

def memb_lipid_cutter(Norm_targets, lip_req, cutoff = 1, lipid_target = False):
    '''
    
    
    '''
    ### If "all" then create Requested list containing all fully named lipids from Norm_targets
    if lip_req == "all":
        lipid_requests = [
            key for key in Norm_targets.keys()
            if key not in [key2[:len(key)] for key2 in Norm_targets.keys() if key != key2]
        ]
    else:
        lipid_requests = lip_req[:]
    
    memb_calc_output = membrane_calculator(Norm_targets = Norm_targets,
                                           requested = lipid_requests,
                                           lipid_target = lipid_target)
    memb_comp = memb_calc_output["memb_comp"]
    memb_sub_comp = memb_calc_output["memb_sub_comp"]
    lipid_removals = []
    partwise_comps = {}
    
    ### While lowest_percentage < cutoff
    removal_number = 0
    while min([memb_comp[key]["percent"] for key in memb_comp.keys()]) <= cutoff:
        ### Finds the key:value combo with the lowest percentage
        lowest_percent = min(memb_comp.items(), key=lambda x: x[1]["percent"])
        lowest_percent_key = lowest_percent[0]
        lowest_percent_percent = lowest_percent[1]["percent"]
        
        
        lipid_removals.append(lowest_percent_key)
        partwise_comps["removel_number: " + str(removal_number)] = {
            "memb_comp": memb_comp,
            "memb_sub_comp": memb_sub_comp
        }
        
        lipid_requests.remove(lowest_percent_key)
        
        memb_calc_output = membrane_calculator(Norm_targets = Norm_targets,
                                               requested = lipid_requests,
                                               lipid_target = lipid_target)
        memb_comp = memb_calc_output["memb_comp"]
        memb_sub_comp = memb_calc_output["memb_sub_comp"]
        
    
    output = {
        "memb_comp": memb_comp,
        "memb_sub_comp": memb_sub_comp,
        "lipid_requests": lipid_requests,
        "lipid_removals": lipid_removals,
        "partwise_comps": partwise_comps,
    }
    
    return output
