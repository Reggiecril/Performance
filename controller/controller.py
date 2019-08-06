import sys

sys.path.append('..')
from tool.readfile import ReadFile
from datetime import datetime
from service.virtualmachine import Virtaulmachine
from service.docker import Docker
from tool.figure import Figure


class Controller(object):
    def __init__(self, time):
        self.vm = Virtaulmachine(time)
        self.docker = Docker(time)
        self.figure_path = '../figure' + time + '/'

    def cpu_test(self):
        test_type = 'cpu'
        self.vm.process(test_type)
        self.docker.process(test_type)
        self.balance(test_type)
        f = Figure(time, test_type, 'sysbench')
        b = Figure(time, test_type, 'vmstat')
        f.two_line_figure(self.vm.sys_time, self.vm.cpu_eps, self.docker.cpu_eps, 'Time', 'Eps', 'eps')
        f.two_line_figure(self.vm.sys_time, self.vm.cpu_lat, self.docker.cpu_lat, 'Time', 'Lat', 'lat')
        f.bar_figure(self.vm.cpu_statistics['CPU_speed']['events_per_second'],
                     self.docker.cpu_statistics['CPU_speed']['events_per_second'], 'Events_Per_Second')
        f.bar_figure(self.vm.cpu_statistics['General_statistics']['total_time'],
                     self.docker.cpu_statistics['General_statistics']['total_time'], 'Total_Time')
        f.bar_figure(self.vm.cpu_statistics['General_statistics']['total_number_of_events'],
                     self.docker.cpu_statistics['General_statistics']['total_number_of_events'],
                     'Total_Number_Of_Events')
        f.bar_figure(self.vm.cpu_statistics['Latency']['sum'], self.docker.cpu_statistics['Latency']['sum'],
                     'Latency_Sum')
        b.two_line_figure(self.vm.sys_time, self.vm.vir_us, self.docker.vir_us, 'Time', 'CPU(%)', 'cpu_percent')

    def memory_test(self):
        test_type = 'memory'
        self.vm.process(test_type)
        self.docker.process(test_type)
        self.balance(test_type)
        f = Figure(time, test_type, 'sysbench')
        b = Figure(time, test_type, 'vmstat')
        f.two_line_figure(self.vm.sys_time, self.vm.memory_usage, self.docker.memory_usage, 'Time', 'Memory_Usage',
                          'memory_usage')
        f.bar_figure(self.vm.memory_statistics['Total_operations'], self.docker.memory_statistics['Total_operations'],
                     'Memory_Read_Time')
        f.bar_figure(self.vm.memory_statistics['General_statistics']['total_time'],
                     self.docker.memory_statistics['General_statistics']['total_time'], 'Total_Time')
        f.bar_figure(self.vm.memory_statistics['General_statistics']['total_number_of_events'],
                     self.docker.memory_statistics['General_statistics']['total_number_of_events'],
                     'Total_Number_Of_Events')
        f.bar_figure(self.vm.memory_statistics['Latency']['sum'], self.docker.memory_statistics['Latency']['sum'],
                     'Latency_Sum')

    def fileio_test(self):
        test_type = 'fileio'
        self.vm.process(test_type)
        self.docker.process(test_type)
        self.balance(test_type)
        f = Figure(time, test_type, 'sysbench')
        b = Figure(time, test_type, 'vmstat')
        ###########fileio#############
        f.two_line_figure(self.vm.sys_time, self.vm.fileio_reads, self.docker.fileio_reads, 'Time', 'fileio_reads',
                          'fileio_reads')
        f.two_line_figure(self.vm.sys_time, self.vm.fileio_writes, self.docker.fileio_writes, 'Time', 'fileio_writes',
                          'fileio_writes')
        f.two_line_figure(self.vm.sys_time, self.vm.fileio_fsyncs, self.docker.fileio_fsyncs, 'Time', 'fileio_fsyncs',
                          'fileio_fsyncs')
        f.two_line_figure(self.vm.sys_time, self.vm.fileio_latency, self.docker.fileio_latency, 'Time', 'fileio_fsyncs',
                          'fileio_latency')
        f.bar_figure(self.vm.fileio_statistics['File_operations']['writes'],
                     self.docker.fileio_statistics['File_operations']['writes'], 'File_Write')
        f.bar_figure(self.vm.fileio_statistics['File_operations']['reads'],
                     self.docker.fileio_statistics['File_operations']['reads'], 'File_Read')
        f.bar_figure(self.vm.fileio_statistics['File_operations']['fsyncs'],
                     self.docker.fileio_statistics['File_operations']['fsyncs'], 'File_Fsyncs')
        f.bar_figure(self.vm.fileio_statistics['General_statistics']['total_time'],
                     self.docker.fileio_statistics['General_statistics']['total_time'], 'total_time')
        f.bar_figure(self.vm.fileio_statistics['General_statistics']['total_number_of_events'],
                     self.docker.fileio_statistics['General_statistics']['total_number_of_events'],
                     'total_number_of_events')
        f.bar_figure(self.vm.fileio_statistics['Latency']['sum'], self.docker.fileio_statistics['Latency']['sum'],
                     'Latency_Sum')
        b.two_line_figure(self.vm.sys_time, self.vm.vir_bi, self.docker.vir_bi, 'Time', 'bi', 'bi')
        b.two_line_figure(self.vm.sys_time, self.vm.vir_bo, self.docker.vir_bo, 'Time', 'bo', 'bo')

    def threads_test(self):
        test_type = 'threads'
        self.vm.process(test_type)
        self.docker.process(test_type)
        self.balance(test_type)
        f = Figure(time, test_type, 'sysbench')
        b = Figure(time, test_type, 'vmstat')
        f.two_line_figure(self.vm.sys_time, self.vm.threads_eps, self.docker.threads_eps, 'Time', 'Eps', 'eps')
        f.two_line_figure(self.vm.sys_time, self.vm.threads_lat, self.docker.threads_lat, 'Time', 'Lat', 'Lat')
        f.bar_figure(self.vm.threads_statistics['Latency']['sum'], self.docker.threads_statistics['Latency']['sum'],
                     'Events_Per_Second')
        f.bar_figure(self.vm.threads_statistics['General_statistics']['total_time'],
                     self.docker.threads_statistics['General_statistics']['total_time'], 'Total_Time')
        f.bar_figure(self.vm.threads_statistics['General_statistics']['total_number_of_events'],
                     self.docker.threads_statistics['General_statistics']['total_number_of_events'],
                     'Total_Number_Of_Events')

    def balance(self, test_type):
        vm_length, docker_length = 0, 0
        if test_type == 'cpu':
            vm_length = len(self.vm.cpu_thds)
            docker_length = len(self.docker.cpu_thds)
            if vm_length != docker_length:
                if vm_length - docker_length < 0:
                    module = self.vm
                else:
                    module = self.docker
                module.cpu_thds.append(0.0)
                module.cpu_eps.append(0.0)
                module.cpu_lat.append(0.0)
                self.balance_vmstat(module)
        elif test_type == 'memory':
            vm_length = len(self.vm.memory_usage)
            docker_length = len(self.docker.memory_usage)
            if vm_length != docker_length:
                if vm_length - docker_length < 0:
                    module = self.vm
                else:
                    module = self.docker
                module.memory_usage.append(0.0)
                self.balance_vmstat(module)
        elif test_type == 'fileio':
            vm_length = len(self.vm.fileio_latency)
            docker_length = len(self.docker.fileio_latency)
            if vm_length != docker_length:
                if vm_length - docker_length < 0:
                    module = self.vm
                else:
                    module = self.docker
                module.fileio_latency.append(0.0)
                module.fileio_fsyncs.append(0.0)
                module.fileio_reads.append(0.0)
                module.fileio_writes.append(0.0)
                self.balance_vmstat(module)
        elif test_type == 'threads':
            vm_length = len(self.vm.threads_eps)
            docker_length = len(self.docker.threads_eps)
            if vm_length != docker_length:
                if vm_length - docker_length < 0:
                    module = self.vm
                else:
                    module = self.docker
                module.threads_lat.append(0.0)
                module.threads_eps.append(0.0)
                module.threads_thds.append(0.0)
                self.balance_vmstat(module)

    def balance_vmstat(self, module):
        module.vir_r.append(0.0)
        module.vir_b.append(0.0)
        module.vir_swpd.append(0.0)
        module.vir_free.append(0.0)
        module.vir_inact.append(0.0)
        module.vir_active.append(0.0)
        module.vir_si.append(0.0)
        module.vir_so.append(0.0)
        module.vir_bi.append(0.0)
        module.vir_bo.append(0.0)
        module.vir_in.append(0.0)
        module.vir_cs.append(0.0)
        module.vir_us.append(0.0)
        module.vir_sy.append(0.0)
        module.vir_id.append(0.0)
        module.vir_wa.append(0.0)
        module.vir_st.append(0.0)


if __name__ == '__main__':
    time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    print time
    c = Controller(time)
    c.cpu_test()
    c.memory_test()
    c.fileio_test()
    c.threads_test()
