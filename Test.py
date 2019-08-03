from template.dockertemplate import Dockertemplate
from tool.property import Property
import ConfigParser
import docker
import datetime
import subprocess
import os
import re


def isnumber(aString):
    try:
        float(aString)
        return True
    except:
        return False
line="[ 5s ] thds: 1 eps: 274.10 lat (ms,95%): 3.75"
line_spilt=line.split(' ')
print line_spilt
for i in line_spilt:
    if isnumber(i):
        print i