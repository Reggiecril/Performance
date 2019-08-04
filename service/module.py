import ConfigParser
import os


class Module(object):
    def __init__(self, time):
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

        # init virtual variable
        self.vir_r, self.vir_b, self.vir_swpd, self.vir_free, self.vir_inact, self.vir_active, self.vir_si, self.vir_so, self.vir_bi, self.vir_bo, self.vir_in, self.vir_cs, self.vir_us, self.vir_sy, self.vir_id, self.vir_wa, self.vir_st = list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list()
        # read property

    def run(self, test_type):
        pass

    def process(self, test_type):
        pass

    def check_test_type(self, test_type):
        if test_type != 'cpu' and test_type != 'memory' and test_type != 'fileio' and test_type != 'threads':
            print "Please enter one of \'cpu\' , \'memory\' , \'fileio\' ,\'threads\'"
            os._exit(0)

    def get_statistics_data(self, dict_statistics, test_type):
        if test_type == 'cpu':
            self.cpu_statistics = dict_statistics
        elif test_type == 'memory':
            self.memory_statistics = dict_statistics
        elif test_type == 'fileio':
            self.fileio_statistics = dict_statistics
        elif test_type == 'threads':
            self.threads_statistics = dict_statistics

    def get_sys_data(self, list_sysbench, test_type):
        # get sysbench stat value
        for i in range(len(list_sysbench)):
            self.sys_time.append(float(list_sysbench[i][0].strip()))
            if test_type == 'cpu':
                self.cpu_thds.append(float(list_sysbench[i][1]))
                self.cpu_eps.append(float(list_sysbench[i][2]))
                self.cpu_lat.append(float(list_sysbench[i][3]))
            elif test_type == 'memory':
                self.memory_usage.append(float(list_sysbench[i][1]))
            elif test_type == 'fileio':
                self.fileio_reads.append(float(list_sysbench[i][1]))
                self.fileio_writes.append(float(list_sysbench[i][2]))
                self.fileio_fsyncs.append(float(list_sysbench[i][3]))
                self.fileio_latency.append(float(list_sysbench[i][4]))
            elif test_type == 'threads':
                self.threads_thds.append(float(list_sysbench[i][1]))
                self.threads_eps.append(float(list_sysbench[i][2]))
                self.threads_lat.append(float(list_sysbench[i][3]))

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

    def read_property(self, test_cfg):
        config_raw = ConfigParser.RawConfigParser()
        config_raw.read(test_cfg)
        return config_raw
