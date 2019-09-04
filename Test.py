from tool.figure import Figure
from tool.module_data import ModuleData
from tool.readfile import ReadFile
def get_modules(test_type,file_name):
    m1=ModuleData('native',test_type,file_name)
    m2=ModuleData('vm',test_type,file_name)
    m3=ModuleData('docker',test_type,file_name)
    return m1,m2,m3
m1,m2,m3=get_modules('cpu','20190809131445997221')
f=Figure('20190809131445997221','cpu')
f.three_line_figure(m1.cpu_lat,m2.cpu_lat,m3.cpu_lat,"Time","THREADS(CPU)",'123')
# print list_pid[0]
# print [i[-4] for i in list_pid1]
