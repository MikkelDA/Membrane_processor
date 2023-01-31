import matplotlib.pyplot as plt
import numpy as np
import math

def pie_plotter(
    memb_dict: dict, # "comp_memb" dictionary
    axs, # <class 'matplotlib.axes._subplots.AxesSubplot'>
    
    colors: dict or "auto" = "auto", # "auto" or key:color dictionary
    
    req_keys: list = [], # List of strings
    excl_keys: list = [], # List of strings
    min_input_key_len: int = 1, # Included minimum length
    max_input_key_len: int = 10, # Included maximum length
    
    min_pie_cut: int = 1, # Minimum pie plotted
    max_pie_cut: int = 10, # Maximum pie plotted
    specific_pie_cut: list = [], # Pie indexes not to be plotted
    join_after_cut: bool = False, # Joins duplicate keys after cuts
    
    norm: bool = True, # True or False
    clean_nestings: False or "remove" or "join" = False, # Cleans the nested pies if only one name on a pie

    simplify_percentages: bool = True, # Removes unnecessary
    text_rotation: bool = False, # Wether text on plot should be rotated
    startangle: int or float = 0, # Start angle given to pie plotter
    rotation_degrees: int or float = 0, # Extra rotations after the above
    
    inner_spacer: int = 2, # Inner "invisible" spacing pies
    pie_thickness: int or float = 1,
    invert_pies: bool = True, # Inverts the nested pie charts
):
    
    axs.axis("equal")
    
    ### Initial labels extracted from dictionary
    init_labels = [
        key
        for key in sorted(list(memb_dict.keys()), key=lambda x: x)
        ### Checks if required keys and excluded keys requirements are fulfilled
        if all([req_key in key for req_key in req_keys]) ### returns true if all true or list is empty
        and not any([excl_key in key for excl_key in excl_keys]) ### Returns false if list is empty
        ### Checks if key length is within limits
        and min_input_key_len <= len(key) <= max_input_key_len
    ]
    
    assert len(init_labels) > 0, '''
    No labels obtained from membrane composition dictionary.
    Either the dictionary is empty or your key requirements are too restrictive:
    (req_keys, excl_keys, min_input_key_len, max_input_key_len)
    '''
    
    min_len = min(len(label) for label in init_labels)
    max_len = max(len(label) for label in init_labels)
    
    data_dicts = {}
    ### Create lists of labels (and plot checks) for all axes up to and including the maximum label length
    for i, length in enumerate(range(1, max_len + 1)):
        data_dicts[length] = {}
        data_dicts[length]["label_lists"] = []
        data_dicts[length]["checker_lists"] = []
        for label in init_labels:
            ### Prevents duplicate entries
            if label[:length] not in data_dicts[length]["label_lists"]:
                data_dicts[length]["label_lists"].append(label[:length])
                if len(label) >= length:
                    data_dicts[length]["checker_lists"].append(True)
                elif len(label) < length:
                    data_dicts[length]["checker_lists"].append(False)
    
    ### Cleans up superfluous nested pies if requested. Joining is done later from "labels_for_joining"
    if clean_nestings in ["remove", "join"]:
        for key in list(data_dicts.keys()):
            if len(set([label[-1] for label in data_dicts[key]["label_lists"]])) == 1:# and (key - 1) in data_dicts.keys():
                backtracker = +1
                while True:
                    if key + backtracker in data_dicts.keys():
                        break
                    else:
                        backtracker += 1
                ### Creates backup list for later use with "join
                data_dicts[key - backtracker]["labels_for_joining"] = data_dicts[key]["label_lists"][0][-1]
                ### Deletes pie axis from dict
                del data_dicts[key]
    
    
    ### ### Color scheme (color map)
    if colors == "auto":
        cmap = plt.colormaps["tab10"]
        colors_cmap = cmap([i for i in range(len(data_dicts[min(data_dicts.keys())]["label_lists"]))])
        colors_dict = {}
        for i, key in enumerate(data_dicts[min(data_dicts.keys())]["label_lists"]):
            colors_dict[key] = colors_cmap[i]
    else: ### Given in function call
        colors_dict = colors
    
    ### Create label and wedge data for plotting
    for key in data_dicts.keys():
        data_dicts[key]["labels_for_plot"] = []
        data_dicts[key]["wedges_for_plot"] = []
        data_dicts[key]["colors_for_plot"] = []
        for j, label in enumerate(data_dicts[key]["label_lists"]):
            ### labels_for_plot
            if clean_nestings == "join" and "labels_for_joining" in data_dicts[key].keys():
                data_dicts[key]["labels_for_plot"].append(" ".join([label[-1], data_dicts[key]["labels_for_joining"]]))
            else:
                data_dicts[key]["labels_for_plot"].append(label[-1])
            
            ### ### Wedge data
            ### Data for wedges with key present in "memb_comp"
            if label in memb_dict.keys():
                data_dicts[key]["wedges_for_plot"].append(memb_dict[label]["percent"] / 100)
            ### Data for wedges that are constructed from above wedges
            else:
                wedges_summed = 0
                for label_2 in data_dicts[max(data_dicts.keys())]["label_lists"]:
                    if label_2[:len(label)] == label:
                        wedges_summed += memb_dict[label_2]["percent"] / 100
                data_dicts[key]["wedges_for_plot"].append(wedges_summed)
            
            ### Colors
            data_dicts[key]["colors_for_plot"].append(colors_dict[label[:min([len(key) for key in colors_dict.keys()])]])
    
    ### ### Cutting away requested pies from min_pie_cut, max_pie_cut and specific_pie_cut
    for key in reversed(list(data_dicts.keys())):
        ### Checks if key should be cut
        min_check = key < min_pie_cut
        max_check = key > max_pie_cut
        specific_check = key in specific_pie_cut
        if any([min_check, max_check, specific_check]):
            ### Joins lower keys (more specific nested pies) together if requested
            if join_after_cut == True:
                ### List of unique identifiers for current key
                identifiers = list(set([label for label in data_dicts[key]["labels_for_plot"]]))
                ### Loops over all keys with more subkeys
                for key2 in list(data_dicts.keys())[key:]:
                    new_data_dicts = {}
                    new_data_dicts["label_lists"] = []
                    new_data_dicts["partial_label_lists"] = []
                    new_data_dicts["identifier_list"] = []
                    new_data_dicts["checker_lists"] = []
                    new_data_dicts["labels_for_plot"] = []
                    new_data_dicts["wedges_for_plot"] = []
                    new_data_dicts["colors_for_plot"] = []
                    
                    
                    for i, label in enumerate(data_dicts[key2]["label_lists"]):
                        ### Finds identifier index
                        identifier_index = 0
                        if identifier_index != 0:
                            break
                        else:
                            for iden in identifiers:
                                if iden in label:
                                    current_iden = iden
                                    iden_index = label.index(iden)
                                    break
                                    
                        ### Creates a partial label to be used as an identifier for subkey combinations
                        partial_label = tuple(
                            [x for j, x in enumerate(data_dicts[key2]["label_lists"][i]) if j != iden_index]
                        )
                        
                        ### Appends new data if partial label has not yet been found
                        if partial_label not in new_data_dicts["partial_label_lists"]:
                            new_data_dicts["partial_label_lists"].append(partial_label)
                            new_data_dicts["identifier_list"].append(current_iden)
                            new_data_dicts["checker_lists"].append(data_dicts[key2]["checker_lists"][i])
                            new_data_dicts["labels_for_plot"].append(data_dicts[key2]["labels_for_plot"][i])
                            new_data_dicts["wedges_for_plot"].append(data_dicts[key2]["wedges_for_plot"][i])
                            new_data_dicts["colors_for_plot"].append(data_dicts[key2]["colors_for_plot"][i])
                        
                        ### Extends data if partial label already found
                        else:
                            new_data_dicts["wedges_for_plot"][new_data_dicts["partial_label_lists"].index(partial_label)] += data_dicts[key2]["wedges_for_plot"][i]
                            new_data_dicts["identifier_list"][new_data_dicts["partial_label_lists"].index(partial_label)] += "_" + current_iden
                    
                    ### Creates new labels from the partial label and the corresponding identifier list
                    for i, label in enumerate(new_data_dicts["partial_label_lists"]):
                        new_label = tuple([
                            *new_data_dicts["partial_label_lists"][i][:iden_index],
                            new_data_dicts["identifier_list"][i],
                            *new_data_dicts["partial_label_lists"][i][iden_index:]
                        ])
                    
                        new_data_dicts["label_lists"].append(new_label)
                    
                    ### Overwrites old data with new joined data
                    data_dicts[key2]["label_lists"] = new_data_dicts["label_lists"]
                    data_dicts[key2]["checker_lists"] = new_data_dicts["checker_lists"]
                    data_dicts[key2]["labels_for_plot"] = new_data_dicts["labels_for_plot"]
                    data_dicts[key2]["wedges_for_plot"] = new_data_dicts["wedges_for_plot"]
                    data_dicts[key2]["colors_for_plot"] = new_data_dicts["colors_for_plot"]
            
            del data_dicts[key]
            

    ### alpha_scaling
    len_difference = len(data_dicts.keys()) + inner_spacer
    axes_alphas = [1 - i for i in np.arange(len_difference) / len_difference]
    
    ### Create alpha and color data for plotting
    for i, key in enumerate(data_dicts.keys()):
        data_dicts[key]["alphas_for_plot"] = []
        for j, label in enumerate(data_dicts[key]["label_lists"]):
            ### Alphas
            if data_dicts[key]["checker_lists"][j] == True:
                data_dicts[key]["alphas_for_plot"].append(axes_alphas[i]) # [- i - inner_spacer - 1]
            else: ### For "invisible" data, e.g. data that should not be seen but is there to take space
                data_dicts[key]["alphas_for_plot"].append(0)
    
    ### ### Plotting the nested pies
    nested_pies = {}
    dict_keys = sorted(list(data_dicts.keys()), reverse = invert_pies)
    for cur_ax, key in enumerate(dict_keys):
        
#         print(cur_ax, key, data_dicts[key]["labels_for_plot"][0])
        nested_pies[cur_ax] = axs.pie(
            data_dicts[key]["wedges_for_plot"],
            radius = axes_alphas[cur_ax] * pie_thickness,
            wedgeprops = dict(
                width = axes_alphas[0] / len_difference * pie_thickness,
                edgecolor = "w",
            ),
            labels = data_dicts[key]["labels_for_plot"],
            labeldistance = 1 - ( 1 / (len(axes_alphas) - cur_ax)) / 2,
            rotatelabels = text_rotation,
            colors = data_dicts[key]["colors_for_plot"],
            startangle = startangle,
            pctdistance = 1 - ( 1 / (len(axes_alphas) - cur_ax)) / 2,
            autopct='%1.1f%%',
            normalize = norm,
        )
        
        ### ### Changes the wedges and labels
        for i, _ in enumerate(nested_pies[cur_ax][0]):
            ### Wedges
            nested_pies[cur_ax][0][i].set(
                alpha = data_dicts[key]["alphas_for_plot"][i]
            )
            
            ### Alpha for text objects
            if data_dicts[key]["alphas_for_plot"][i] == 0:
                textalph = 0
            else:
                textalph = 1
            
            ### Text size
            text_size = 2 + 4 * max(data_dicts[key]["alphas_for_plot"])
            
            
            no_percent = False
            (l_ha, l_va, l_r), (p_ha, p_va, p_r) = (("center", "bottom", "anchor"), ("center", "top", "anchor"))
            
            ### Checks if percentage should be shown in case of only 1 derivative of upper subkey
            if simplify_percentages == True and key != min(data_dicts.keys()):
                checker = []
                
                for label in data_dicts[key]["label_lists"]:
                    backtracker = -1
                    while True:
                        if key + backtracker in data_dicts.keys():
                            break
                        else:
                            backtracker -= 1
    
                    self_unique = data_dicts[key]["label_lists"][i][:backtracker] == label[:backtracker]
                    if all([self_unique]):
                        checker.append(True)
                    else:
                        checker.append(False)
                if sum(checker) == 1:
                    no_percent = True
                    (l_ha, l_va, l_r), (p_ha, p_va, p_r) = (("center", "center", "default"), ("center", "center", "default"))
            
            ### ### Labels
            ### Calculate rotation
            rotation_degrees = rotation_degrees
            x_pos, y_pos = nested_pies[cur_ax][1][i].get_position()
            cur_rot = nested_pies[cur_ax][1][i].get_rotation()
            if text_rotation == True:
                new_rot = cur_rot - math.copysign(1, x_pos) * math.copysign(1, y_pos) * rotation_degrees
            elif text_rotation == False:
                new_rot = cur_rot + math.copysign(1, x_pos) * rotation_degrees
            
            ### Key label
            nested_pies[cur_ax][1][i].set(
                size = text_size,
                ha = l_ha,
                va = l_va,
                alpha = textalph,
                rotation = new_rot,
                rotation_mode = l_r,
            )
            ### Percentages
            if len(nested_pies[cur_ax]) > 2 and no_percent == False:
                nested_pies[cur_ax][2][i].set(
                    size = text_size,
                    ha = p_ha,
                    va = p_va,
                    alpha = textalph,
                    rotation = nested_pies[cur_ax][1][i].get_rotation(),
                    rotation_mode = p_r,
                )
            else:
                nested_pies[cur_ax][2][i].set(
                    alpha = 0,
                )
    return nested_pies
