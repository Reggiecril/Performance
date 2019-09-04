from tool.readfile import ReadFile


class ModuleData(object):
    def __init__(self,module,test_type,file_name):
        self.test_type=test_type
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
        self.vir_user, self.vir_system, self.vir_guest, self.vir_cpu_percent, self.vir_cpu, self.vir_minflt, self.vir_majflt, self.vir_vsz, self.vir_rss, self.vir_mem, self.vir_rd, self.vir_wr, self.vir_ccwr = list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list()

        self.get_des(module,file_name)
    def get_statistics_data(self, dict_statistics):
        if self.test_type == 'cpu':
            self.cpu_statistics = dict_statistics
        elif self.test_type == 'memory':
            self.memory_statistics = dict_statistics
        elif self.test_type == 'fileio':
            self.fileio_statistics = dict_statistics
        elif self.test_type == 'threads':
            self.threads_statistics = dict_statistics

    def get_sys_data(self, list_sysbench):
        self.sys_time = list()
        # get sysbench stat value
        for i in range(len(list_sysbench)):
            self.sys_time.append(float(list_sysbench[i][0].strip()))
            if self.test_type == 'cpu':
                self.cpu_thds.append(float(list_sysbench[i][1]))
                self.cpu_eps.append(float(list_sysbench[i][2]))
                self.cpu_lat.append(float(list_sysbench[i][3]))
            elif self.test_type == 'memory':
                self.memory_usage.append(float(list_sysbench[i][1]))
            elif self.test_type == 'fileio':
                self.fileio_reads.append(float(list_sysbench[i][1]))
                self.fileio_writes.append(float(list_sysbench[i][2]))
                self.fileio_fsyncs.append(float(list_sysbench[i][3]))
                self.fileio_latency.append(float(list_sysbench[i][4]))
            elif self.test_type == 'threads':
                self.threads_thds.append(float(list_sysbench[i][1]))
                self.threads_eps.append(float(list_sysbench[i][2]))
                self.threads_lat.append(float(list_sysbench[i][3]))

    def get_vir_data(self, list_virstat):
        # init virtual variable
        self.vir_user, self.vir_system, self.vir_guest, self.vir_cpu_percent, self.vir_cpu, self.vir_minflt, self.vir_majflt, self.vir_vsz, self.vir_rss, self.vir_mem, self.vir_rd, self.vir_wr, self.vir_ccwr = list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list()
        # get vir stat value
        for j in range(len(list_virstat)):
            self.vir_user.append(float(list_virstat[j][0]))
            self.vir_system.append(float(list_virstat[j][1]))
            self.vir_guest.append(float(list_virstat[j][2]))
            self.vir_cpu_percent.append(float(list_virstat[j][3]))
            self.vir_cpu.append(float(list_virstat[j][4]))
            self.vir_minflt.append(float(list_virstat[j][5]))
            self.vir_majflt.append(float(list_virstat[j][6]))
            self.vir_vsz.append(float(list_virstat[j][7]))
            self.vir_rss.append(float(list_virstat[j][8]))
            self.vir_mem.append(float(list_virstat[j][9]))
            self.vir_rd.append(float(list_virstat[j][10]))
            self.vir_wr.append(float(list_virstat[j][11]))
            self.vir_ccwr.append(float(list_virstat[j][12]))

    def get_des(self,module, file_name):
        r1 = ReadFile("file/" + module + "/" + self.test_type + "/sysbench/" + file_name + ".txt")
        r2 = ReadFile("file/" + module + "/" + self.test_type + "/pidstat/" + file_name + ".log")
        list_sysbench, dict_statistics = r1.read_sysbench_file()
        list_pid = r2.read_pidstat_file()
        self.get_sys_data(list_sysbench)
        self.get_vir_data(list_pid)
        self.get_statistics_data(dict_statistics)