import subprocess
import sys
import os

def installRequirementsWithPip():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    subprocess.call([sys.executable,"-m", "pip", "install", "-r", "requirements.txt"])

installRequirementsWithPip()
