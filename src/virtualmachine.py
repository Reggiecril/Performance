import sys

from src.docker import Docker

sys.path.append('..')
from tool.linefigure import LineFigure
from tool.readfile import ReadFile
from template.vmtemplate import VMTemplate
from datetime import datetime
from tool.property import Property
import ConfigParser


class Virtaulmachine():
    def __init__(self,time):
        # (%Y-%m-%d %H:%M:%S%f)
        self.now_time = time
        self.config_raw = self.read_property("../property.ini")
        # sysbench variable
        self.sys_time = list()

        # for sysbench CPU test
        self.cpu_thds, self.cpu_eps, self.cpu_lat = list(), list(), list()
        self.cpu_statistics = dict()
        # for sysbench Memory test
        self.memory_usage = list()
        self.memory_statistics = dict()
        # for sysbench Fileio test
        self.fileio_reads, self.fileio_writes, self.fileio_fsyncs, self.fileio_latency = list(), list(), list(), list()
        self.fileio_statistics = dict()
        # for sysbench Threads test
        self.threads_thds, self.threads_eps, self.threads_lat = list(), list(), list()
        self.threads_statistics = dict()


    # read property
    def read_property(self, test_cfg):
        config_raw = ConfigParser.RawConfigParser()
        config_raw.read(test_cfg)
        return config_raw

    def run(self):
        v = Property(True)
        t = VMTemplate(v.db_cmd(), v.sys_cmd(), v.vir_stat(), v.clear_db_cmd())
        t.get_result()
        f = open("../file/vm/" + self.config_raw.get("Parameter", "threads") + "-" + self.now_time + ".txt", "w")
        f.write(t.sysbench + '\n' + t.stat)

    def process(self):
        self.run()
        list_sysbench, list_virstat = ReadFile(True,
            "../file/vm/" + self.config_raw.get("Parameter", "threads") + "-" + self.now_time + ".txt").read_file()
        self.get_sys_data(list_sysbench)
        self.get_vir_data(list_virstat)

    def get_sys_data(self, list_sysbench):
        self.sys_thds = list_sysbench[0][1]
        # get sysbench stat value
        for i in range(len(list_sysbench)):
            self.sys_timeseries.append(float(list_sysbench[i][0]))
            self.sys_tps.append(float(list_sysbench[i][2]))
            self.sys_qps.append(float(list_sysbench[i][3]))
            self.sys_lat.append(float(list_sysbench[i][4]))
            self.sys_err.append(float(list_sysbench[i][5]))
            self.sys_reconn.append(float(list_sysbench[i][6]))

    def get_vir_data(self, list_virstat):
        # get vir stat value
        for j in range(len(list_virstat)):
            self.vir_r.append(float(list_virstat[j][0]))
            self.vir_b.append(float(list_virstat[j][1]))
            self.vir_swpd.append(float(list_virstat[j][2]))
            self.vir_free.append(float(list_virstat[j][3]))
            self.vir_inact.append(float(list_virstat[j][4]))
            self.vir_active.append(float(list_virstat[j][5]))
            self.vir_si.append(float(list_virstat[j][6]))
            self.vir_so.append(float(list_virstat[j][7]))
            self.vir_bi.append(float(list_virstat[j][8]))
            self.vir_bo.append(float(list_virstat[j][9]))
            self.vir_in.append(float(list_virstat[j][10]))
            self.vir_cs.append(float(list_virstat[j][11]))
            self.vir_us.append(float(list_virstat[j][12]))
            self.vir_sy.append(float(list_virstat[j][13]))
            self.vir_id.append(float(list_virstat[j][14]))
            self.vir_wa.append(float(list_virstat[j][15]))
            self.vir_st.append(float(list_virstat[j][16]))


if __name__ == '__main__':
    time =datetime.now().strftime("%Y%m%d%H%M%S%f")
    print time
    v = Virtaulmachine(time)
    v.process()
    d= Docker(time)
    d.process()
    f = LineFigure()
    f.two_line(["vm"],[])
    # f.multi_line([["tps", v.sys_timeseries, v.vir_sy, "b"], ["qps", v.sys_timeseries, v.vir_us, "r"],
    #               ["lat", v.sys_timeseries, v.vir_so, "r"]], 'Time', 'TPS and QPS', "../figure/VM-" + v.now_time)
