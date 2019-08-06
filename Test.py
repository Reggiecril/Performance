from template.dockertemplate import Dockertemplate
from tool.figure import Figure
from tool.property import Property
import ConfigParser
from datetime import datetime
import subprocess
import os
import re

from tool.readfile import ReadFile


class Test(object):
    def __init__(self, module_type, test_type, file_name):
        self.module_type = module_type
        self.test_type = test_type
        self.file_name = file_name
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

    def get_data(self):
        path = 'file/' + self.module_type + '/' + self.test_type + '/' + self.file_name
        list_sysbench, list_virstat, dict_statistics = ReadFile(path).read_file()
        self.get_sys_data(list_sysbench, self.test_type)
        self.get_vir_data(list_virstat)
        self.get_statistics_data(dict_statistics, self.test_type)

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

if __name__ == '__main__':
    test_type = 'fileio'
    #file 20190804181824944975
    # cpu 20190804181153507882
    #memory 20190804175945634648
    #threads 20190804182218899623
    file_name = '20190804181824944975.txt'
    vm = Test('vm', test_type, file_name)
    vm.get_data()
    docker = Test('docker', test_type, file_name)
    docker.get_data()
    time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    print time

    f = Figure(time,test_type,'sysbench')
    b= Figure(time,test_type,'vmstat')
    ###########fileio#############
    f.two_line_figure(vm.sys_time, vm.fileio_reads, docker.fileio_reads, 'Time', 'fileio_reads', 'fileio_reads')
    f.two_line_figure(vm.sys_time, vm.fileio_writes, docker.fileio_writes, 'Time', 'fileio_writes', 'fileio_writes')
    f.two_line_figure(vm.sys_time, vm.fileio_fsyncs, docker.fileio_fsyncs, 'Time', 'fileio_fsyncs', 'fileio_fsyncs')
    f.two_line_figure(vm.sys_time, vm.fileio_latency, docker.fileio_latency, 'Time', 'fileio_fsyncs', 'fileio_latency')
    f.bar_figure(vm.fileio_statistics['File_operations']['writes'], docker.fileio_statistics['File_operations']['writes'],'File_Write')
    f.bar_figure(vm.fileio_statistics['File_operations']['reads'], docker.fileio_statistics['File_operations']['reads'],'File_Read')
    f.bar_figure(vm.fileio_statistics['File_operations']['fsyncs'], docker.fileio_statistics['File_operations']['fsyncs'],'File_Fsyncs')
    f.bar_figure(vm.fileio_statistics['General_statistics']['total_time'], docker.fileio_statistics['General_statistics']['total_time'],'total_time')
    f.bar_figure(vm.fileio_statistics['General_statistics']['total_number_of_events'], docker.fileio_statistics['General_statistics']['total_number_of_events'],'total_number_of_events')
    f.bar_figure(vm.fileio_statistics['Latency']['sum'], docker.fileio_statistics['Latency']['sum'],'Latency_Sum')
    b.two_line_figure(vm.sys_time, vm.vir_bi, docker.vir_bi, 'Time', 'bi', 'bi')
    b.two_line_figure(vm.sys_time, vm.vir_bo, docker.vir_bo, 'Time', 'bo', 'bo')
    # ###########memory#############
    # f.two_line_figure(vm.sys_time, vm.memory_usage, docker.memory_usage, 'Time', 'Memory_Usage', 'memory_usage.png')
    # f.bar_figure(vm.memory_statistics['Total_operations'], docker.memory_statistics['Total_operations'],'Memory_Read_Time')
    # f.bar_figure(vm.memory_statistics['General_statistics']['total_time'], docker.memory_statistics['General_statistics']['total_time'],'Total_Time')
    # f.bar_figure(vm.memory_statistics['General_statistics']['total_number_of_events'], docker.memory_statistics['General_statistics']['total_number_of_events'],'Total_Number_Of_Events')
    # f.bar_figure(vm.memory_statistics['Latency']['sum'], docker.memory_statistics['Latency']['sum'],'Latency_Sum')
    #
    # ###########cpu#############
    # f.two_line_figure(vm.sys_time, vm.cpu_eps, docker.cpu_eps, 'Time', 'Eps', 'eps')
    # f.two_line_figure(vm.sys_time, vm.cpu_lat, docker.cpu_lat, 'Time', 'Lat', 'lat')
    # f.bar_figure(vm.cpu_statistics['CPU_speed']['events_per_second'], docker.cpu_statistics['CPU_speed']['events_per_second'],'Events_Per_Second')
    # f.bar_figure(vm.cpu_statistics['General_statistics']['total_time'], docker.cpu_statistics['General_statistics']['total_time'],'Total_Time')
    # f.bar_figure(vm.cpu_statistics['General_statistics']['total_number_of_events'], docker.cpu_statistics['General_statistics']['total_number_of_events'],'Total_Number_Of_Events')
    # f.bar_figure(vm.cpu_statistics['Latency']['sum'], docker.cpu_statistics['Latency']['sum'],'Latency_Sum')
    # b.two_line_figure(vm.sys_time,vm.vir_us,docker.vir_us,'Time','CPU(%)','cpu_percent')
    #
    # ###########threads#############
    # f.two_line_figure(vm.sys_time, vm.threads_eps, docker.threads_eps, 'Time', 'Eps', 'eps')
    # f.two_line_figure(vm.sys_time, vm.threads_lat, docker.threads_lat, 'Time', 'Lat', 'Lat')
    # f.bar_figure(vm.threads_statistics['Latency']['sum'], docker.threads_statistics['Latency']['sum'],'Events_Per_Second')
    # f.bar_figure(vm.threads_statistics['General_statistics']['total_time'], docker.threads_statistics['General_statistics']['total_time'],'Total_Time')
    # f.bar_figure(vm.threads_statistics['General_statistics']['total_number_of_events'], docker.threads_statistics['General_statistics']['total_number_of_events'],'Total_Number_Of_Events')