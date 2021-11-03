import os
from simpleeval import simple_eval
from _argparse import Argparse


argparse = Argparse(description="Basic but useful CLI tools.")

@argparse.add_command(
    metavar="<filename>", help="Create a new empty file.", dest='-mkfile'
)
def mkfile_command(string):
    current_directory = os.getcwd()
    file_directory = os.path.join(current_directory, string)
    if os.path.exists(file_directory):
        print("Path already exists.")
    else:
        open(file_directory, "w").close()
        print("File has been created.")


@argparse.add_command(
    metavar="<expression>",
    help="Safely evaluate an expression. Could be used as a basic calculator too.",
    dest='-eval'
)
def eval_command(string):
    execution = simple_eval(string)
    print(execution)

argparse.instigate()
