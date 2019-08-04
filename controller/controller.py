import sys

sys.path.append('..')
from tool.linefigure import LineFigure
from tool.readfile import ReadFile
from datetime import datetime
from service.virtualmachine import Virtaulmachine
from service.docker import Docker


class Controller(object):
    def __init__(self, time):
        self.vm = Virtaulmachine(time)
        self.docker = Docker(time)

    def cpu_test(self):
        self.vm.process('cpu')
        print self.vm.sys_time
        print self.vm.cpu_thds, self.vm.cpu_eps, self.vm.cpu_lat
        print self.vm.cpu_statistics
        self.docker.process('cpu')
        print self.docker.sys_time
        print self.docker.cpu_thds, self.docker.cpu_eps, self.docker.cpu_lat
        print self.docker.cpu_statistics
    def memory_test(self):
        self.vm.process('memory')
        print self.vm.sys_time
        print self.vm.memory_usage
        print self.vm.memory_statistics
        self.docker.process('memory')
        print self.docker.sys_time
        print self.docker.memory_usage
        print self.docker.memory_statistics

    def fileio_test(self):
        self.vm.process('fileio')
        print self.vm.sys_time
        print self.vm.fileio_reads, self.vm.fileio_writes, self.vm.fileio_fsyncs, self.vm.fileio_latency
        print self.vm.fileio_statistics
        self.docker.process('fileio')
        print self.docker.sys_time
        print self.docker.fileio_reads, self.docker.fileio_writes, self.docker.fileio_fsyncs, self.docker.fileio_latency
        print self.docker.fileio_statistics

    def threads_test(self):
        self.vm.process('threads')
        print self.vm.sys_time
        print self.vm.threads_thds, self.vm.threads_eps, self.vm.threads_lat
        print self.vm.threads_statistics
        self.docker.process('threads')
        print self.docker.sys_time
        print self.docker.threads_thds, self.docker.threads_eps, self.docker.threads_lat
        print self.docker.threads_statistics

if __name__ == '__main__':
    time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    print time
    c = Controller(time)
    c.threads_test()
