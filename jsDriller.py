# jsDriller.py <file>

import re
import base64
import jsbeautifier
import sys
import itertools



def return_function_name(function_content):
    return str(re.findall("(\\w+)\\(.*?\\)\\{", function_content)).replace("[", "").replace("'", "").replace("]", "")

file_name = sys.argv[1]
global variables_checked
file_name = file_name
file = open(file_name, "r").read()
file_lines = open(file_name, "r").readlines()
file = file.replace(" ", "").replace("\n", "")

normal_functions = re.findall("function(\w+)\(", file)
functions_contents = re.findall("function(.*?\\(.*?\\){.*?})", file)
functions_inside_dictionaries = re.findall("'\\w+':function\\(.*?\\)", file)
functions_as_variable = re.findall("\\w+=function\\(.*?\\)", file)
if_statements = re.findall("if\\(.*?{.*?}", file)
variables = re.findall("var(.*?)=", file)
try_blocks = re.findall("try{(.*?)}", file)
else_statements = re.findall("else{(.*?)}", file)
strings = re.findall("\'.*?'|\".*?\"", file)

report = {
    
    # "normal_functions": normal_functions,
    # "functions_contents": functions_contents,
    # "functions_inside_dictionaries": functions_inside_dictionaries,
    # "functions_as_variable": functions_as_variable,
    # "if_statements": if_statements,
    # "variables": set(variables),
    # "try_blocks": try_blocks,
    # "else_statements": else_statements,
    # "strings": strings,
    #
    # # Not really working the regex
    # "base_64_strings": re.findall("(?:[A-Za-z0-9+\\/]{4}\\n?)*(?:[A-Za-z0-9+\\/]{2}==|[A-Za-z0-9+\\/]{3}=)", file),

    "variables_inside_functions": set(),
    "variables_inside_if": set(),
    "variables_inside_else": set(),
    "variables_inside_try": set(),

    "inside_functions": 0,
    "inside_if": 0,
    "inside_else": 0,
    "inside_try": 0,
}

variable_count = \
    [

    ]

variables_checked = set()
variables_checked2 = set()
functions_checked = set()
functions_checked2 = set()

for variable in variables:
    for function_content in functions_contents:
        id = return_function_name(str(function_content))
        if variable in str(function_content):
            # report["variables_inside_functions"].add(f"Variable {variable} found inside {return_function_name(str(function_content))}, count: {str(function_content).count(variable)}")
            report["variables_inside_functions"].add(variable)
        report["inside_functions"] = len(report["variables_inside_functions"])
    for if_content in if_statements:
        if variable in if_content:
            report["variables_inside_if"].add(variable)
        report["inside_if"] = len(report["variables_inside_if"])
    for else_content in else_statements:
        if variable in else_content:
            report["variables_inside_else"].add(variable)
        report["inside_else"] = len(report["variables_inside_else"])
    for try_content in try_blocks:
        if variable in try_content:
            report["variables_inside_try"].add(variable)
        report["inside_try"] = len(report["variables_inside_try"])

    line_count = 0
    for line in file_lines:
        line_count += 1
        if variable in line.strip():
            if file.count(variable) == 1:
                variables_checked.add(f"{variable} is unused and found at {line_count}")
                variables_checked2.add(variable)
                
for function_content in functions_contents:
    line_count = 0
    for line in file_lines:
        line_count += 1
        function_name = return_function_name(function_content)
        if function_name in line.strip():
            if file.count(function_name) == 1:
                functions_checked.add(f"Function {function_name} is unused and fount at {line_count}")
                functions_checked.add(function_name)
            

js_beautify = jsbeautifier.beautify_file(file_name)
for variable in variables_checked2:
    js_beautify = str(js_beautify).replace(variable, "unused")
for function_name in functions_checked:
    js_beautify = str(js_beautify).replace(function_name, "unused")

print(f"""
Report:
{report} 
Code:
{js_beautify}
Unused Variables:
{list(variables_checked)}
Unused Functions:
{list(functions_checked)}
""")
