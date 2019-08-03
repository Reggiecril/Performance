from template.dockertemplate import Dockertemplate
from tool.property import Property
import ConfigParser
import docker
import datetime
import subprocess
import os
import re


def vm_data(line):
    l = line.split(" ")
    count = 0
    while count < len(l):
        if l[count] == " " or l[count] == "":
            l.pop(count)
        else:
            count += 1
    return l


string=" 1  0 101500  71836 119136 246512    0    0     0     0  280  173 100  0  0  0  0"
print string.strip()
print len(vm_data(string.strip()))