#!/usr/bin/env python3

# system packages

import json
import os
import functions
import datetime
import pprint
import pandas as pd
import sys

def gen_timestamp_id():
    id = datetime.datetime.now().strftime("%Y.%d.%m:%H:%M.%S.%f")
    return(id)

def get_package_name(install_path):
    """
    Pass in an installation path string and get back the last folder
    which is the name of the package. Eg. rincewind
    """
    package_name = install_path.split('/')
    return(package_name[-2])

def create_local_dir(dirname):
    cwd = os.getcwd()
    dirToCreate = cwd + "/." + dirname + "/"
    try:
        os.mkdir(dirToCreate)
    except FileExistsError:
       # print(f"Folder exists")
        pass
    return(dirToCreate)

def create_command_file(local_command_cache):
    now = datetime.datetime.now()
    time = now.strftime("%Y-%m-%d_%H_%M.%f")
    filename = local_command_cache + time + ".bash"
    fh = open(filename,"w")
    return(fh)

def check_command_exists(command_dict, command_name):
    """
    Checks if a given command exists in the dictionary.
    If this does not then prints a general help.
    """
    try:
        present_command = command_dict[command_name]
        return(present_command)
    except KeyError:
        print(f"command '{command_name}' not found")
        package_help(command_dict)
        exit(1)


def check_command_exists(command_objects, command_name):
    """
    Checks if a given command exists in the dictionary.
    If this does not then prints a general help.
    """
    try:
        command_names = [ c.name for c in command_objects]
        command_ob = [ c for c in command_objects if c.name in command_name ]
        if len(command_ob) > 1:
            print(f"error: {command_name} found more than once")
            exit(1)
        else:
            return(command_ob[0])
    except KeyError:
        print(f"command '{command_name}' not found")
        package_help(command_dict)
        exit(1)

def get_type_separator(types, character = "-"):
    times = len(list(types))
    v = character * times
    return(v)

def package_help(command_dict):
    print("""
    Available commands are ...
    """)
    commands_df = pd.DataFrame()
    for k in command_dict.keys():
        command_metadata = command_dict[k]
        df = pd.DataFrame(command_metadata)
        df = df.reset_index()
        df = df[["command_name", "type","short_help"]]
        df = df.drop_duplicates()
        commands_df = commands_df.append(df)
    types_of_commands = list(commands_df["type"].unique())
    for types in types_of_commands:
        type_data = commands_df[commands_df['type'] == types]
        print(types)
        print(get_type_separator(types))
        for i,r in type_data.iterrows():
            print("{0}:\t{1}".format(r['command_name'], r['short_help']))
    
def get_conf_files(install_path):
    file_command_line_options = install_path + "/conf/command_line_options.txt"
    file_main_conf = install_path + "/conf/main.conf"
    commands_json = install_path + "conf/commands.json"
    conf_dict = {
        "command_line_options": file_command_line_options, 
        "main_conf": file_main_conf,
        "commands_json": commands_json
    }
    return(conf_dict)

def get_command_line_options(options_file):
    # options_file = configs['command_line_options']
    temp = pd.read_csv(options_file, sep= "\t", header= 0)
    temp = temp.dropna(how = "all") # drop if all values in a row are NaN
    return(temp)

def print_command_line_options(command_line_options):
    print(command_line_options)

class Command:
    def __init__(self, k,v):
        self.name = v['command_name']
        self.type = v['type']
        self.command = v['command']
        self.short_help = v['short_help']
        self.long_help = v['long_help']
        self.mandatory_args = v['mandatory_args']
        self.optional_args = v['optional_args']

    def command_line(self):
        return(self.command)
    
    def command_name(self):
        return(self.name)
    
    def create_command_file(self, local_command_cache):
        now = datetime.datetime.now()
        time = now.strftime("%Y-%m-%d_%H_%M.%f")
        filename = local_command_cache + time + ".bash"
        print(r"Writing in file : ${filename}")
        fh = open(filename,"w")
        return(fh)

    # print out the command
    def bashing(self):
        local_command_cache=create_local_dir(package_name)
        local_command_file = create_command_file(local_command_cache)
        print(present_command.command_line(), file = local_command_file)
        local_command_file.close()
        return()

    
#* Input vars
install_path="/Users/vm11/SOFT/rincewind/" # Must be pulled in as env var
cwd = os.getcwd()

try:
    install_path=os.environ['__installdir']
except KeyError:
    print("Your install directory is not set.")
    print(os.environ)
    exit(0)

#* Get package name
package_name = get_package_name(install_path = install_path)

#* Create local cache
local_cache_dir = cwd + "/." + package_name + "/"
create_local_dir(package_name)

#* Get the main configuration file paths
configs = get_conf_files(install_path)

#* Reading in json file that has all the commands listed
commands_json= configs['commands_json']
with open(commands_json, "r") as fh:
    commands = json.load(fh)


#** Creating a list of command objects
command_objects = []
for k,v in commands.items():
    print(k)
    command_objects.append(Command(k,v))

# check args
command_line_options = get_command_line_options(configs['command_line_options'])
print_command_line_options(command_line_options)
exit(0)



# Get the command name
command_name = "searchfile" # Supply from main bash
#print(sys.argv)
#command_name = sys.argv[0]

#*  


# --> "commands" is a dictionary of commands

#### Check if command exists
present_command = check_command_exists(command_objects, command_name)

# print out the command
local_command_cache=create_local_dir(package_name)

# pass on the command file to bash
local_command_file = create_command_file(local_command_cache)
print(present_command['command'], file = local_command_file)
local_command_file.close()
