# # # # run sysbench to test
import sys
from service.virtualmachine import Virtaulmachine

time =sys.argv[1]
print time
v=Virtaulmachine(time)
v.process('cpu')
v.process('memory')
v.process('fileio')
v.process('threads')