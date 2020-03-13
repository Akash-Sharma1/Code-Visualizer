import sys
import inspect
import os
import time
from datetime import datetime
import copy, argparse
import importlib

class var_infos:
    def __init__(self, name, line, step, value):
        self.name = name
        self.line_value = []
        self.appendto_logs(line, step, value)
        
    def appendto_logs(self, line, step, value):
        self.line_value.append({"line" : line, "step" : step, "value" : value})
    
    def getvariabletype(self):
        value = self.line_value[0]["value"]
        var_type = type(value)
        for lv in self.line_value:
            if type(lv["value"]) != var_type:
                return "undefined" # if all variable types are not same
        return var_type
    
    def range(self):
        if self.getvariabletype() in [int, float]:
            values = [ lv["value"] for lv in self.line_value ]
            return [min(values), max(values)]
        else:
            return []
    
    def all_vals(self):
        return {
            "var" : self.name,
            "type": str(self.getvariabletype()),
            "range": self.range(),
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
        self.step = 0
        
        
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
        if frame.f_code.co_name == self.function_name:
            return self._trace_lines_
    
    def _trace_lines_(self, frame, event, args):
        curr_logs = {
            "step": self.step,
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
                    {"action": "init_var", "var": var, "val": val})
                
                self.var_logs[var] = var_infos( var, self.curr_line, self.step, copy.deepcopy(val))
                
            elif self.prev_vars[var] != val:
                prev_val = self.prev_vars[var]
                
                if isinstance(prev_val, list) and isinstance(val, list):
                    self.debuglist(var, prev_val, val)
                elif isinstance(prev_val, dict) and isinstance(val, dict):
                    self.debugdict(var, prev_val, val)
                else:
                    curr_logs["actions"].append(
                        {"action": "change_var", "var": var, "prev_val": prev_val, "new_val": val})
                self.var_logs[var].appendto_logs(
                    self.curr_line, self.step, copy.deepcopy(val))

        self.prev_vars = copy.deepcopy(current_variables)
        self.prev_time = time.time()
        self.curr_line = frame.f_lineno
        self.step += 1

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
        # print(module),
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

        logs = self.results["logs"]
        for step in logs:
            print(
                "Step {}, line {}".format(
                step["step"], step["line_num"],)
            )

            print("", end="")
            if step["actions"]:
                first = True
                for action in step["actions"]:
                    if first:
                        first = False
                    else:
                        print(", ", end="")

                    if action["action"] == "init_var":
                        action_desc = "variable '{}' created and initiated with {}".format(
                            action["var"], action["val"])
                    elif action["action"] == "change_var":
                        action_desc = "variable '{}' changed from {} to {}".format(
                            action["var"], action["prev_val"], action["new_val"])
                    elif action["action"] == "rm_var":
                        action_desc = "variable '{}' is deleted from memory {} to {}".format(
                            action["var"], action["prev_val"], action["None"])
                    elif action["action"] == "list_add":
                        action_desc = "{}[{}] appended with value {}".format(
                            action["var"], action["index"], action["val"])
                    elif action["action"] == "list_change":
                        action_desc = "{}[{}] changed from {} to {}".format(
                            action["var"], action["index"], action["prev_val"], action["new_val"])
                    elif action["action"] == "list_remove":
                        action_desc = "{}[{}] removed".format(
                            action["var"], action["index"])
                    elif action["action"] == "dict_add":
                        action_desc = "key {} added to {} with value {}".format(
                            action["key"], action["var"], action["val"])
                    elif action["action"] == "dict_change":
                        action_desc = "value of key {} in {} changed from {} to {}".format(
                            action["key"], action["var"], action["prev_val"], action["new_val"])
                    elif action["action"] == "dict_remove":
                        action_desc = "key {} removed from {}".format(
                            action["key"], action["var"])
                    print(action_desc, end="")
                print("")
        print()

        linelogs = self.results["line_logs"]
        print("", end="")
        for line in linelogs:
            print("Line {}:".format(line))
        print("", end="")


def funcarg(argument):
    try:
        return int(argument)
    except ValueError:
        try:

            return float(argument)
        except ValueError:
            return argument

debugpwd = "test.py"
function_name = "test2"
function_args = []

tdebugger = debugC(debugpwd, function_name, function_args, [])

results = tdebugger.run()

terminal = Terminal(results)
terminal.terminal()