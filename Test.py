from template.dockertemplate import Dockertemplate
from tool.property import Property
import ConfigParser
import datetime
import subprocess
import os
import re

from tool.readfile import ReadFile

r = ReadFile('file/20190803222023348522.txt')
a,b,c=r.read_file()
for i in a:
    print i