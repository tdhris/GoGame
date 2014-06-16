import os
from subprocess import call

WORKINGDIR = os.getcwd();
for file in os.listdir(WORKINGDIR):
    if file.endswith("_tests.py"):
        print("\nExecuting : " + file)
        call("python " + file, shell=True)
