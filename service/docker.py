from tool.readfile import ReadFile
from template.dockertemplate import Dockertemplate
from datetime import datetime
import ConfigParser
from module import Module


class Docker(Module):
    def __init__(self, time):
        super(Docker, self).__init__(time)
    def run(self, test_type):

        t = Dockertemplate('docker', test_type,self.now_time)
        t.run()
        sysbench_path="./file/docker/" + test_type + '/' +'sysbench/'+ self.now_time + ".txt"
        self.check_path(sysbench_path)
        f = open(sysbench_path, "w")
        f.write(t.sysbench)

    def process(self, test_type):
        self.check_test_type(test_type)
        self.run(test_type)
        # list_sysbench,dict_statistics = ReadFile("./file/docker/" + test_type + '/'+'sysbench/' + self.now_time + ".txt").read_sysbench_file()
        # list_virstat=ReadFile("./file/docker/" + test_type + '/'+'pidstat/'+ self.now_time + ".log").read_pidstat_file()
        # print list_sysbench, dict_statistics
        # print list_virstat
        # self.get_sys_data(list_sysbench,test_type)
        # self.get_vir_data(list_virstat)
        # self.get_statistics_data(dict_statistics,test_type)

# if __name__ == '__main__':
#     time = datetime.now().strftime("%Y%m%d%H%M%S%f")
#     print time
#     v = Docker(time)
#     v.process('cpu')
#     print v.cpu_thds, v.cpu_eps, v.cpu_lat
#     print v.vir_r, v.vir_b, v.vir_swpd, v.vir_free, v.vir_inact, v.vir_active, v.vir_si, v.vir_so, v.vir_bi, v.vir_bo, v.vir_in, v.vir_cs, v.vir_us, v.vir_sy, v.vir_id, v.vir_wa, v.vir_st
#     sys.exit(0)
