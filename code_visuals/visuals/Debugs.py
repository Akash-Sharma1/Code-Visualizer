import sys
import inspect
import os
import time
from datetime import datetime
import copy, argparse
import importlib

class var_infos:
    def __init__(self, name, line, value):
        self.name = name
        self.line_value = []
        self.appendto_logs(line, value)
        
    def appendto_logs(self, line, value):
        self.line_value.append({"line" : line, "value" : value})
    
    def getvariabletype(self):
        value = self.line_value[0]["value"]
        var_type = type(value)
        for lv in self.line_value:
            if type(lv["value"]) != var_type:
                return "undefined" # if all variable types are not same
        return var_type
    
    def all_vals(self):
        return {
            "var" : self.name,
            "type": str(self.getvariabletype()),
            "line_value": self.line_value
        }
    
class debugC:
    def __init__(self, file_path, function_name, function_args, custom_args):
        self.file_path = file_path
        self.function_name = function_name
        self.function_args = function_args
        self.custom_arguments = custom_args
        
        self.curr_line = None
        
        self.prev_vars = {}
        self.var_logs = {}# storing variable objects
        self.line_logs = {}# stores encountred lines
        
        self.prev_time = time.time()
        
        self.results = {
            "code_info": {
                "filename": os.path.split(self.file_path)[1],
                "function_name": self.function_name,
                "function_args": self.function_args,
                "custom_arguments": self.custom_arguments
                },
            "logs": [],
            "var_logs": [],
            "line_logs": []
        }
        
    def _trace_calls_(self, frame, event, args):
        self.curr_line = frame.f_lineno
        if frame.f_code.co_name == self.function_name: # this limits to one funtion only
            return self._trace_lines_
    
    def _trace_lines_(self, frame, event, args):
        curr_logs = {
            "line_num": self.curr_line,
            "actions": []
        }
        self.results["logs"].append(curr_logs)
        
        if self.curr_line not in self.line_logs:# if curr line_num not is encountered lines add it to lines_logs.
            self.line_logs[self.curr_line] = self.curr_line
        
        self.first_print_for_this_line = True
        current_variables = frame.f_locals
        
        for var, val in current_variables.items():
            if var not in self.prev_vars: # if new variable encountered add it to actions under initializing variables
                curr_logs["actions"].append(
                    {"action": "init_var", "var": var, "val": copy.deepcopy(val)})
                
                self.var_logs[var] = var_infos( var, self.curr_line, copy.deepcopy(val))
                
            elif self.prev_vars[var] != val:
                prev_val = self.prev_vars[var]
                
                if isinstance(prev_val, list) and isinstance(val, list):
                    self.debuglist(var, prev_val, val)
                elif isinstance(prev_val, dict) and isinstance(val, dict):
                    self.debugdict(var, prev_val, val)
                else:
                    curr_logs["actions"].append(
                        {"action": "change_var", "var": var, "prev_val": prev_val, "new_val": val})
                
                self.var_logs[var].appendto_logs( self.curr_line, copy.deepcopy(val))

        self.prev_vars = copy.deepcopy(current_variables)
        self.prev_time = time.time()
        self.curr_line = frame.f_lineno

    def debuglist(self, var, prev_val, val):
        curr_logs = self.results["logs"][-1]

        for i in range(min(len(val), len(prev_val))):
            if val[i] != prev_val[i]:
                curr_logs["actions"].append(
                    {"action": "list_change", "var": var, "index": i, "prev_val": prev_val[i], "new_val": val[i]})
        if len(val) > len(prev_val):
            for i in range(len(prev_val), len(val)):
                curr_logs["actions"].append(
                    {"action": "list_add", "var": var, "index": i, "val": val[i]})
        if len(val) < len(prev_val):
            for i in range(len(val), len(prev_val)):
                curr_logs["actions"].append(
                    {"action": "list_remove", "var": var, "index": i})

    def debugdict(self, var, prev_val, val):
        curr_logs = self.results["logs"][-1]

        for elem in val:
            if elem not in prev_val:
                curr_logs["actions"].append(
                    {"action": "dict_add", "var": var, "key": elem, "val": val[elem]})
            elif prev_val[elem] != val[elem]:
                curr_logs["actions"].append(
                    {"action": "dict_change", "var": var, "key": elem, "prev_val": prev_val[elem], "new_val": val[elem]})
        for elem in prev_val:
            if elem not in val:
                curr_logs["actions"].append(
                    {"action": "dict_remove", "var": var, "key": elem})

    def run(self):
        module_spec = importlib.util.spec_from_file_location(
            "debugger", self.file_path)
        module = importlib.util.module_from_spec(module_spec)
        
        module_spec.loader.exec_module(module)
        function = getattr(module, self.function_name)

        sys.settrace(self._trace_calls_)
        sys.argv = self.custom_arguments
        self.prev_time = time.time()

        self.results["arguments"] = function(*self.function_args)
        sys.settrace(None)

        self.results["var_logs"] = [var_obj.all_vals() for var_obj in self.var_logs.values()]
        self.results["line_logs"] = [line_obj for line_obj in self.line_logs.values()]

        return self.results
    
class Terminal:
    def __init__(self, results):
        self.results = results

    def terminal(self):
        
        
        ans = []

        logs = self.results["logs"]
        for step in logs:
            
            temp = {"Line": str( step["line_num"] ) , "actions": []}
            
            if step["actions"]:
                for action in step["actions"]:
                    
                    One_step = {}
                    
                    ##########################intialization
                    
                    if action["action"] == "init_var":
                        
                        One_step["about"] = "Intialize"
                        One_step["var_name"] = action["var"]
                        One_step["val"] = action["val"]
                        type_var = str(type(action["val"]))
                        One_step['val_type'] = type_var[ type_var.find("'")+1 : type_var.find("'",type_var.find("'")+1 ) ]
                        
                    ############################adding
                        
                    elif action["action"] == "list_add":
                        
                        One_step["about"] = "Add"
                        One_step["var_name"] = action["var"]
                        One_step["val"] = action["val"]
                        One_step["index"] = action["index"]
                        One_step["var_type"] = "List"
                        type_var = str(type(action["val"]))
                        One_step['val_type'] = type_var[ type_var.find("'")+1 : type_var.find("'",type_var.find("'")+1 ) ]
                    
                    elif action["action"] == "dict_add":
                        
                        One_step["about"] = "Add"
                        One_step["var_name"] = action["var"]
                        One_step["val"] = action["val"]
                        One_step["key"] = action["key"]
                        One_step["var_type"] = "Dict"
                        type_var = str(type(action["val"]))
                        One_step['val_type'] = type_var[ type_var.find("'")+1 : type_var.find("'",type_var.find("'")+1 ) ]
                    
                    #########################change
                    
                    elif action["action"] == "change_var": # whole variable is changed
                        
                        One_step["about"] = "Change"
                        One_step["var_name"] = action["var"]
                        One_step["new_val"] = action["new_val"]
                        One_step["prev_val"] = action["prev_val"]
                        One_step["var_type"] = "Variable"
                        type_var = str(type(action["new_val"]))
                        One_step['val_type'] = type_var[ type_var.find("'")+1 : type_var.find("'",type_var.find("'")+1 ) ]
                        
                    elif action["action"] == "list_change":
                        
                        One_step["about"] = "Change"
                        One_step["var_name"] = action["var"]
                        One_step["index"] = action["index"]
                        One_step["new_val"] = action["new_val"]
                        One_step["prev_val"] = action["prev_val"]
                        One_step["var_type"] = "List"
                        type_var = str(type(action["new_val"]))
                        One_step['val_type'] = type_var[ type_var.find("'")+1 : type_var.find("'",type_var.find("'")+1 ) ]
                    
                    elif action["action"] == "dict_change":
                        
                        One_step["about"] = "Change"
                        One_step["var_name"] = action["var"]
                        One_step["key"] = action["key"]
                        One_step["new_val"] = action["new_val"]
                        One_step["prev_val"] = action["prev_val"]
                        One_step["var_type"] = "Dict"
                        type_var = str(type(action["new_val"]))
                        One_step['val_type'] = type_var[ type_var.find("'")+1 : type_var.find("'",type_var.find("'")+1 ) ]
                    
                    #########################remove
                
                    elif action["action"] == "list_remove":
                        
                        One_step["about"] = "Remove"
                        One_step["var_name"] = action["var"]
                        One_step["index"] = action["index"]
                        One_step["var_type"] = "List"
                        
                    elif action["action"] == "dict_remove":
                        One_step["about"] = "Remove"
                        One_step["var_name"] = action["var"]
                        One_step["key"] = action["key"]
                        One_step["var_type"] = "Dict"
                    
                    temp["actions"].append(One_step)

            ans.append(temp)

        linelogs = self.results["line_logs"]

        return ans        
        


def main():

    debugpwd = "visuals/to_debug.py"
    function_name = "main"
    function_args = []

    rundebug = debugC(debugpwd, function_name, function_args, [])

    results = rundebug.run()

    terminal = Terminal(results)
    output = terminal.terminal()
    
    print(output)
    for i in output:
        print( i["Line"])
        for j in i["actions"]:
            print(j)
    return output
    

if __name__ == "__main__":
    main()

# # represents line number
# L represents list
# D represents dictionary
# V represents variable
# = represents initalization
# + represents appending
# - represents removing
# : represents key value pair
# => represents  prev value to new value
