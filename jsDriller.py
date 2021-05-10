import re
import base64
import jsbeautifier



def return_function_name(function_content):
    return str(re.findall("(\\w+)\\(.*?\\)\\{", function_content))


file_name = "test.txt"
file = open(file_name, "r").read()
file = file.replace(" ", "").replace("\n","")


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
    "normal_functions": normal_functions,
    "functions_contents": functions_contents,
    "functions_inside_dictionaries": functions_inside_dictionaries,
    "functions_as_variable": functions_as_variable,
    "if_statements": if_statements,
    "variables": set(variables),
    "try_blocks": try_blocks,
    "else_statements": else_statements,
    "strings": strings,

    # Not really working the regex
    "base_64_strings": re.findall("(?:[A-Za-z0-9+\\/]{4}\\n?)*(?:[A-Za-z0-9+\\/]{2}==|[A-Za-z0-9+\\/]{3}=)", file),

    "variables_inside_functions": set(),
    "variables_inside_if": set(),
    "variables_inside_else": set(),
    "variables_inside_try": set(),
}

variable_count = \
    [

    ]


for variable in variables:
    for function_content in functions_contents:
        id = return_function_name(str(function_content))
        if variable in str(function_content):
            report["variables_inside_functions"].add(
                f"Variable {variable} found inside {return_function_name(str(function_content))}, count: {str(function_content).count(variable)}")
    for if_content in if_statements:
        if variable in if_content:
            report["variables_inside_if"].add(f"Variable {variable} found inside {jsbeautifier.beautify(if_content)}, count: {str(if_content).count(variable)}")
    for else_content in else_statements:
        if variable in else_content:
            report["variables_inside_else"].add(f"Variable {variable} found inside {else_content}, count: {str(else_content).count(variable)}")
    for try_content in try_blocks:
        if variable in try_content:
            report["variables_inside_try"].add(f"Variable {variable} found inside {try_content}, , count: {str(try_content).count(variable)}")

file = open(f"analysis_{file_name}.txt", "a")
file.write(str(report) + "\n"*10)
file.write(jsbeautifier.beautify_file(file_name))
file.close()

print(jsbeautifier.beautify(report["if_statements"][0]))
