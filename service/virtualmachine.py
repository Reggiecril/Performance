from module import Module
from template.vmtemplate import VMTemplate
from tool.readfile import ReadFile
from datetime import datetime

class Virtaulmachine(Module):
    def __init__(self, time):
        super(Virtaulmachine, self).__init__(time)

    def run(self, test_type):
        t = VMTemplate(True, test_type)
        t.run()
        f = open("../file/vm/" + test_type + '/' + self.now_time + ".txt", "w")
        f.write(t.sysbench + '\n' + t.stat)

    def process(self, test_type):
        self.run(test_type)
        list_sysbench, list_virstat,dict_statistics = ReadFile("../file/vm/" + test_type + '/' + self.now_time + ".txt").read_file()
        self.get_sys_data(list_sysbench,test_type)
        self.get_vir_data(list_virstat)
        self.get_statistics_data(dict_statistics, test_type)

# if __name__ == '__main__':
#     time =datetime.now().strftime("%Y%m%d%H%M%S%f")
#     print time
#     v = Virtaulmachine(time)
#     v.process("cpu")
#     print v.cpu_thds, v.cpu_eps, v.cpu_lat
#     print v.vir_r, v.vir_b, v.vir_swpd, v.vir_free, v.vir_inact, v.vir_active, v.vir_si, v.vir_so, v.vir_bi, v.vir_bo, v.vir_in, v.vir_cs, v.vir_us, v.vir_sy, v.vir_id, v.vir_wa, v.vir_st
#     sys.exit(0)
#     # f.multi_line([["tps", v.sys_timeseries, v.vir_sy, "b"], ["qps", v.sys_timeseries, v.vir_us, "r"],
#     #               ["lat", v.sys_timeseries, v.vir_so, "r"]], 'Time', 'TPS and QPS', "../figure/VM-" + v.now_time)
