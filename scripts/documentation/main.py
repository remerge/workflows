import os
import argparse
import yaml
from yaml.constructor import SafeConstructor
from yaml.reader import *
from yaml.scanner import *
from yaml.parser import *
from yaml.composer import *
from yaml.resolver import *
from string import Template
from typing import Tuple
from pathlib import Path
from names_generator import generate_name

parser = argparse.ArgumentParser()
parser.add_argument("--path", "-p", help="path to workflows", required=True)

# https://stackoverflow.com/a/58593978
# Create custom safe constructor class that inherits from SafeConstructor
class MySafeConstructor(SafeConstructor):
    # Create new method handle boolean logic
    def add_bool(self, node):
        return self.construct_scalar(node)

class MySafeLoader(Reader, Scanner, Parser, Composer, MySafeConstructor, Resolver):
    def __init__(self, stream):
        Reader.__init__(self, stream)
        Scanner.__init__(self)
        Parser.__init__(self)
        Composer.__init__(self)
        MySafeConstructor.__init__(self)
        Resolver.__init__(self)

# Inject the above boolean logic into the custom constuctor
MySafeConstructor.add_constructor('tag:yaml.org,2002:bool',
                                      MySafeConstructor.add_bool)

def get_value(value: str,default: str) -> str :
    if value != None:
        return value
    return default

def generate_data(file_path: str) -> Tuple[str, str]:
    file = open(file_path, 'r')
    file_name = Path(file_path).name

    description = ""
    while True:
        # Get next line from file
        line = file.readline()
        # if line doesnt start with #
        # break out
        if not line.startswith("#"):
            break
        description += "{}".format(line.strip().strip("#"))

    file.close()

    with open(file_path) as f:
        data = yaml.load(f,MySafeLoader)

    name = get_value(data.get("name"),file_name)

    template = Template(
        """
## $name
---
$description
### Snippet
$snippet
### Inputs
$inputs
### Secrets
$secrets
        """
    )

    snippet_template = Template(
        """
```
name: $project_name
on:
  push:
    branches: [ '*' ]
jobs:
  test:
    uses: remerge/workflows/.github/workflows/$file_name@main
    $inputs
    $secrets
```"""
    )


    # if workflow_call is not set then it is not a reusable workflow
    # and should be skipped
    if "workflow_call" not in data.get("on"):
        return None,None

    inputs = data.get("on").get("workflow_call").get("inputs")
    input_str = ""
    inputs_sample = ""
    if inputs != None:
        inputs_sample += "with:\r"
        for input in inputs:
            input_data = inputs.get(input)
            input_type = input_data.get("type")
            is_required = input_data.get("required")
            inputs_sample += "\t\t{}: {} value (required:{})\r".format(
                input,
                input_type,
                is_required
            )
            input_str += """
* **{0}**
    * **Description:** {1}
    * **Type:** *{2}*
    * **Required:** *{3}*
    * **Default:** *{4}*
            """.format(
                get_value(input,file_path),
                get_value(input_data.get("description"),"N/A"),
                input_type,
                is_required,
                get_value(input_data.get("default"),"N/A"),
            )

    secrets = data.get("on").get("workflow_call").get("secrets")
    secret_str = ""
    secrets_sample = ""
    if secrets != None:
        secrets_sample += "secrets:\r"
        for secret in secrets:
            secret_data = secrets.get(secret)
            is_secret_required = secret_data.get("required")
            secrets_sample += "\t\t{}: secret value (required:{})\r".format(secret,is_secret_required)
            secret_str += """
* **{0}**
    * **Description:** {1}
    * **Required:** *{2}*
            """.format(
                get_value(secret,"N/A"),
                get_value(secret_data.get("description"),"N/A"),
                is_secret_required,
            )
    snippet = snippet_template.substitute(
        {
            'inputs': inputs_sample,
            'secrets': secrets_sample,
            'file_name': file_name,
            'project_name': generate_name(style='capital'),
        }
    )
    return name , template.substitute(
        {
            'name': name,
            'snippet': snippet,
            'description': description,
            'inputs': input_str,
            'secrets': secret_str,
        }
    )

args = parser.parse_args()
path = args.path
files = os.listdir(path)
files.sort()

list_of_workflows = "# Available Reusable Workflows \n"
workflow_str = ""


for file in files:
    result = generate_data(path+file)
    if result[0] == None:
        continue
    list_of_workflows += "* [{}](#{}) \n".format(result[0],result[0].replace(" ","-"))
    workflow_str += result[1]

print( "**Note:** *This page is autogenerated.*\n")
print(list_of_workflows)
print(workflow_str)