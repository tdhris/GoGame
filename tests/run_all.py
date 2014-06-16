import os
from platform import python_version
from subprocess import call

WORKINGDIR = os.getcwd()
for file in os.listdir(WORKINGDIR):
    if file.endswith("_tests.py"):
        print("\nExecuting : " + file)
        if python_version().startswith('3.'):
            command = "python3"
        elif python_version().startswith('2.'):
            command = "python"
        call(command + " " + file, shell=True)
