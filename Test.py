# # # # run sysbench to test
import ConfigParser
import subprocess
import os
import shutil
import sys
from datetime import datetime

# import re
#
from service.docker import Docker
from service.native import Native
from service.virtualmachine import Virtaulmachine
time = datetime.now().strftime("%Y%m%d%H%M%S%f")
print time
v=Virtaulmachine(time)
v.process('memory')
print len(v.vir_cpu_percent)

# v.process('cpu')
# print len(v.vir_cpu_percent)
#
# v.process('threads')
# print len(v.vir_cpu_percent)
#
# v.process('fileio')
# print len(v.vir_cpu_percent)
