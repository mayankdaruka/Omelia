import functions
from value_types import *

def run_functions(curr_spreadsheet, query_string, query_parameters):
    print("Query string: " + query_string)
    # ADD <ENTRY_1> <ENTRY_2>
    # <ENTRY_1>: row 4
    commands = query_string.split(".")
    sheet = curr_spreadsheet.sheet
    for i in range(len(commands)):
        args_and_comm = commands[i].split(" ")
        command_name = args_and_comm[0]
        args = []

        for k in range(1, len(args_and_comm)):
            result = args.append(query_parameters[args_and_comm[k]])

        result = None
        
        if command_name == "ADD":
            result = functions.add(sheet, args[0], args[1])
        elif command_name == "INSERTAFT":
            if args[0].rowOrCol == 'col':
                result = functions.insert_entry(sheet, chr(ord(args[0].value) + 1), args[0].rowOrCol)
            else:
                result = functions.insert_entry(sheet, int(args[0].value) + 1, args[0].rowOrCol)
        elif command_name == "INSERTBEF":
            if args[0].rowOrCol == 'col':
                result = functions.insert_entry(sheet, chr(ord(args[0].value)), args[0].rowOrCol)
            else:
                result = functions.insert_entry(sheet, int(args[0].value), args[0].rowOrCol)
        elif command_name == "SET":
            if(isinstance(args[0], float)):
                result = functions.cell_update(sheet, args[1].cell_str, args[0])
            else:
                result = functions.cell_update(sheet, args[1].cell_str, args[0].value)
        elif command_name == "AVG":
            result = functions.average_entry(sheet, args[0].value, args[0].rowOrCol)
        elif command_name == "BOLD":
            if(isinstance(args[0], Cell)):
                result = functions.format_bold(sheet, str(args[0].cell_str) + ":" + str(args[0].cell_str))
            else:
                result = functions.format_bold_entry(sheet, args[0])
        elif command_name == "SET_BG":
            if(len(args) == 2):
                if(isinstance(args[1], Cell)):
                    result = functions.set_background(sheet, args[1].cell_str + ":" + args[1].cell_str, args[0].color_str)
                else:
                    result = functions.set_background_entry(sheet, args[1], args[0].color_str)
            else:
                result = functions.set_background(sheet, str(args[1].cell_str) + ":" + str(args[2].cell_str), args[0].color_str)
        elif command_name == "MULTIPLY":
            if(isinstance(args[1], Entry)):
                result = functions.multiply_entry(sheet, int(args[0].value), args[1].value, args[1].rowOrCol == "row")
            else:
                result = functions.multiply_cell(sheet, int(args[0].value), args[1].cell_str)
        elif command_name == "SIN":
            if(len(args) == 1):
                if (isinstance(args[0], Cell)):
                    result = functions.sin_cell(sheet, args[0].cell_str)
                else:
                    # Don't know if this works
                    result = functions.sin_entry(sheet, ord(args[0].value) - ord("A") + 1, args[0].rowOrCol == "col")
            else:
                result = functions.sin_range(sheet, str(args[0].cell_str) + ":" + str(args[1].cell_str))
        elif command_name == "COS":
            if(len(args) == 1):
                if (isinstance(args[0], Cell)):
                    result = functions.cos_cell(sheet, args[0].cell_str)
                else:
                    result = functions.cos_entry(sheet, args[0].value, args[0].rowOrCol == "col")
            else:
                result = functions.cos_range(sheet, str(args[0].cell_str) + ":" + str(args[1].cell_str))
        elif command_name == "SORT":
            # result = functions.sort(sheet, args[0])
            if(args[0].rowOrCol == 'col'):
                result = functions.sort(sheet, (ord(args[0].value) - ord("A") + 1, 'asc'))
        # elif command_name == "FILTER_EVEN":
        #     result = functions.filter_even(sheet, args[0])
        # elif command_name == "FILTER_ODD":
        #     result = functions.filter_odd(sheet, args[0])
        elif command_name == "FILTER_PRIME":
            result = functions.filter_by_prime(sheet)
        # elif command_name == "MAX_VAL":
        #     result = functions.max_val(sheet, args[0])
        # elif command_name == "NORMALIZE":
        #     result = functions.normalize(sheet, args[0], args[1])
        
        query_parameters["<RES_" + str(i + 1) + ">"] = result