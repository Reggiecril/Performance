import sys
sys.path.append('..')
from tool.linefigure import LineFigure
from tool.readfile import ReadFile
from template.dockertemplate import Dockertemplate
from datetime import datetime
import ConfigParser
from module import Module


class Docker(Module):
    def __init__(self, time):
        super(Docker, self).__init__(time)
    def run(self, test_type):

        t = Dockertemplate(False, test_type)
        t.run()
        f = open("../file/docker/" + test_type + '/' + self.now_time + ".txt", "w")
        f.write(t.sysbench + '\n' + t.stat)

    def process(self, test_type):
        self.check_test_type(test_type)
        self.run(test_type)
        list_sysbench, list_virstat = ReadFile(
            False, "../file/docker/" + test_type + '/' + self.now_time + ".txt").read_file()
        self.get_sys_data(list_sysbench)
        self.get_vir_data(list_virstat)

if __name__ == '__main__':
    time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    print time
    v = Docker(time)
    v.process('cpu')
    print v.cpu_thds, v.cpu_eps, v.cpu_lat
    print v.vir_r, v.vir_b, v.vir_swpd, v.vir_free, v.vir_inact, v.vir_active, v.vir_si, v.vir_so, v.vir_bi, v.vir_bo, v.vir_in, v.vir_cs, v.vir_us, v.vir_sy, v.vir_id, v.vir_wa, v.vir_st
    sys.exit(0)
