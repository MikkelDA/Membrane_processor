
def print_helper():
    ### ### ### ### ### ### ### ### Helper ("-h" or "--help") begin ### ### ### ### ### ### ### ###
    helper = []
    no_space = 0
    space_1 = 3
    space_2 = 6
    space_3 = 11
    space_4 = 14
    helper.append(((no_space,), ("Possible input files:",)))
    # helper.append(((no_space,), (" ",)))
    helper.append(((space_2,), ("-N (Required) Input file containing a complete set of normalization parameters.",)))
    # helper.append(((no_space,), (" ",)))

    helper.append(((space_3,), ("Guide on writing an input file containing normalization parameters:",)))
    helper.append(((space_4,), ("The file can contain empty lines and comments using '#'.",
                            "Parameters contain two parts (key and value) and a separator (:) resulting in key:value.",
                            "Note that the rightmost ':' on a line is used as separator, meaning that a key can contain ':'.",)))
    # helper.append(((no_space,), (" ",)))
    helper.append(((space_3,), ("Key:",)))
    helper.append(((space_4,), ("Each key must follow a logical 'left-to-right' order of indexing where each",
                            "index to the left of a given index must be separately defined with a ratio value.",
                            "Indexes in keys are separated by a comma ','.",)))
    helper.append(((space_4,), ("Keys can contain 'all' which results in this key being created for all keys with the same",
                            "prior key indexes (to the left of 'all').",)))
    helper.append(((space_4,), ("Keys can also contain parenthesis (specifically round  parenthesis '(elements)'),",
                            "which forces the key to be generated for each element within the parenthesis separately.",)))
    helper.append(((space_4,), ("See the examples below for a demonstration.",)))
    helper.append(((space_3,), ("Ratio:",)))
    helper.append(((space_4,), ("The ratio value can be represented either as a number (integer or float) (such as 5 or 7.6)",
                            "or as a mix of summations and/or subtractions (ex: 37.7 + 4.9 + 3.4 - 17.9).",
                            "Note that the the values are RATIOS and not PERCENTAGES, meaning that they do not need",
                            "to equal any specific number. The ratio for the lipids chosen to make a membrane",
                            "are normalized both partway through the calculations and at the end towards 100%.",)))
    helper.append(((space_3,), ("Example:",)))
    helper.append(((space_4,), ("PL: 46.8",)))
    helper.append(((space_4,), ("ST: 37.7 + 4.9 + 3.4",)))
    helper.append(((space_4,), ("PL,Outer: 35",)))
    helper.append(((space_4,), ("PL,Inner: 65",)))
    helper.append(((space_4,), ("ST,Outer: 70",)))
    helper.append(((space_4,), ("ST,Inner: 30",)))
    helper.append(((space_4,), ("PL,all,PC: 35.5 # Creates: 'PL,Outer,PC: 35.5' and 'PL,Inner,PC: 35.5'",)))
    helper.append(((space_4,), ("PL,all,PE: 5.5",)))
    helper.append(((space_4,), ("PL,all,PG: 9.0",)))
    helper.append(((space_4,), ("PL,all,PC,18:0:18:0: 18.7",)))
    helper.append(((space_4,), ("PL,all,PE,18:0:18:0: 16.3",)))
    helper.append(((space_4,), ("PL,all,PG,18:0:18:0: 9.1",)))
    helper.append(((space_4,), ("PL,all,(PC,PG),18:0:18:1: 19.3",)))
    helper.append(((space_4,), ("# Above creates 'PL,all,PC,18:0:18:1: 19.3', 'PL,all,PG,18:0:18:1: 19.3'",)))
    helper.append(((space_4,), ("PL,all,PE,18:0:18:1: 17.3",)))
    helper.append(((space_4,), ("ST,all,FS: 37.7",)))
    ### ### ### Output stuff
    helper.append(((no_space,), (" ",)))
    helper.append(((no_space,), ("Possible output files:",)))
    helper.append(((space_1,), ("At least one output file (flags starting with an 'o') must be provided.",)))
    helper.append(((space_2,), ("-o (optional) Output file wherein the membrane composition will be written.",)))
    helper.append(((no_space,), (" ",)))
    helper.append(((space_2,), ("-oI (optional) Output file in a format usable in for the Insane script.",)))
    helper.append(((no_space,), (" ",)))
    helper.append(((space_2,), ("-oL (optional) Output file in a latex table format.",)))
    helper.append(((no_space,), (" ",)))
    helper.append(((space_2,), ("-log (optional) Log file.",)))

    ### ### ### Membrane-lipid commands
    helper.append(((no_space,), (" ",)))
    helper.append(((no_space,), ("Membrane-lipid commands:",)))
    helper.append(((space_2,), ("-L (repeatable) Lipid for the membrane.",)))
    helper.append(((space_3,), ("Structure of '-L' flag:",)))
    helper.append(((space_4,), ("'-L full_lipid_identifier-subcommand_1-subcommand_2' etc.",)))
    helper.append(((space_3,), ("Subcommands for '-L' flag:",)))
    helper.append(((space_4,), ("SR:Percentage - Scales the lipid normalization target by 'Percentage' (integer or float)",)))
    helper.append(((space_3,), ("Examples of '-L' flag usage:",)))
    helper.append(((space_4,), ("'-L PL,Outer,PC,16:0:18:2' - Normal request with no subcommands",)))
    helper.append(((space_4,), ("'-L PL,Outer,PC,16:0:18:2-SR:500' - Ratio scaled by 500%",)))
    helper.append(((space_4,), ("'-L PL,Inner,PC,16:0:18:2-SR:500' - 'Inner' instead of 'Outer'",)))
    helper.append(((space_4,), ("The two commands above can be given as separate flags:",)))
    helper.append(((space_4,), ("'-L PL,Outer,PC,16:0:18:2-SR:500 -L PL,Inner,PC,16:0:18:2-SR:500'",)))
    helper.append(((space_4,), ("or combined into one flag:",)))
    helper.append(((space_4,), ("'-L PL,(Outer,Inner),PC,16:0:18:2-SR:500'",)))
    helper.append(((no_space,), (" ",)))
    helper.append(((space_2,), ("-L_file (repeatable) File(s) containing lipids for the membrane.",)))
    helper.append(((space_3,), ("Lines can be empty and contain comments (similar to '-N' files)",)))
    helper.append(((space_4,), ("Lipid requests should be formatted similarly to the '-L' flag but",
                            "without the '-L' and with only one lipid command per line. '-L'",
                            "and '-L_file' flags can be used at the same time",)))
    helper.append(((no_space,), (" ",)))
    helper.append(((space_2,), ("-LT (optional, integer) Calculate number of lipids with this number as a target.",)))
    helper.append(((space_3,), ("Effectively just normalizes the lipid percentages towards this",
                            "number, after which each lipid has their new percentage rounded using",
                            "pythons 'round()' function",)))
    helper.append(((space_3,), ("This value can be defined in the '-L_file' file by having a line like this:",)))
    helper.append(((space_3,), ("lipid_target = 430",)))
    helper.append(((space_3,), ("If the '-LT' flag is supplied while 'lipid_target' is defined in '-L_file' then",
                            "the value from '-LT' will be used")))
    helper.append(((space_3,), ("If multiple 'lipid_target' are supplied in '-L_file' file(s) then the last defined will be used")))
    helper.append(((no_space,), (" ",)))
    helper.append(((space_2,), ("-C (optional, repeatable) Changes normalization ratio value for single lipid",)))
    helper.append(((space_3,), ("This flag can also be used to add new lipids one at a time to normalization dictionary",)))
    helper.append(((space_3,), ("Examples of '-C' flag usage:",)))
    helper.append(((space_4,), ("'-C PL,Outer:50' changes 'PL,Outer' from the original 65 to 50",)))

    ### ### ### ### ### ### ### ### Helper end ### ### ### ### ### ### ### ###

    def print_line_formatter(string, max_length, front_spacer):
        if type(string) == tuple:
            string = " ".join(string)
        string = string.replace("  ", " ")
        string_chunks = [string[i:i + max_length - front_spacer].lstrip(" ").rstrip(" ") for i in range(0, len(string), max_length - front_spacer)]
        for chunk in string_chunks:
            print(" " * front_spacer, chunk)
    
    max_length = 90
    for (settings, parts) in helper:
        front_spacer = settings[0]
        print_line_formatter(parts, max_length, front_spacer)

### ### ### ### Prints to terminal
def terminal_printer(memb_comp, decimals = 3, lambda_for_sort = None, sort_rev = False):
    header = ["Lipid nr", "Dictionary key", "Membrane percentage"]
    lipids_present = all([any([key2 == "lipids" for key2 in memb_comp[key].keys()]) for key in memb_comp.keys()])
    if lipids_present:
        header = header +  ["Lipid composition", "Lipid percentage"]

    if lambda_for_sort == None:
        lambda_for_sort = lambda x: x
    
    lines = []
    lines.append(header)
    for i, key in enumerate(sorted(memb_comp.keys(),
                                   key = lambda_for_sort,
                                   reverse = sort_rev)):
        line = []
        line.append(str(i))
        line.append(str(key))
        line.append(str(round(memb_comp[key]["percent"], decimals)))
        if lipids_present:
            line.append(str(memb_comp[key]["lipids"]))
            line.append(str(round(memb_comp[key]["lipids_percent"], decimals)))
        lines.append(line)
    
    max_lengths = [max([len(line[i]) for line in lines]) for i in range(len(lines[0]))]
    tot_length = max(max_lengths)
    for line in lines:

        for i, i_text in enumerate(line):
            i_text_len = int(max_lengths[i]) - len(i_text)
            text = i_text + i_text_len * " "
            print(text, end = "   ")
        print()

