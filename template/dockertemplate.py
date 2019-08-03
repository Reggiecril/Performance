
import subprocess
import time
import os
from template import Template


class Dockertemplate(Template):
    def __init__(self, vm_type,test_type):
        super(Dockertemplate, self).__init__(vm_type,test_type)
    def fileio_prepared(self):
        default=self.config_raw.defaults()
        test = self.get_test(self.test_type)
        parameter = self.get_command(self.get_vm_option_list(self.config_raw.options("Parameter")), "Parameter")
        cmd = default['docker_run'] + ' ' + default['docker_image'] + ' ' + default[
            'sys_name'] + ' ' + self.test_type + ' ' + test + ' ' + parameter + ' prepared'
        os.system(cmd)
    def fileio_clean(self):

        test = self.get_test(self.test_type)
        parameter = self.get_command(self.get_vm_option_list(self.config_raw.options("Parameter")), "Parameter")
        cmd = self.default['docker_run'] + ' ' + self.default['docker_image'] + ' ' + self.default[
            'sys_name'] + ' ' + self.test_type + ' ' + test + ' ' + parameter + ' cleanup'
        os.system(cmd)

    def run_sysbench_vir(self, sys_cmd, vir_stat):
        # run sysbench to test
        p1 = subprocess.Popen(sys_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # returncode of p1, if return is None means subprocess is running,if returncode is 0 means subprocess is finised
        returncode = p1.poll()
        sysbench_stat, docker_stat = list(), list()
        # during excuting, get information of p1
        while returncode is None:
            # get sysbench data
            sysbench_line = p1.stdout.readline().strip()
            returncode = p1.poll()
            print sysbench_line
            if sysbench_line == "Threads started!":
                break
        while True:
            # get sysbench data
            sysbench_line = p1.stdout.readline().strip()
            sysbench_stat.append(sysbench_line)

            # run docker stats
            p2 = subprocess.Popen(vir_stat, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            # get docker data
            docker_line = p2.stdout.readline().strip()
            docker_stat.append(docker_line)
            # print datetime.datetime.now().second, docker_line
            # print sysbench_line
            if sysbench_line.strip()=='':
                continue
            if sysbench_line.strip().split(' ')[0]=='execution':
                break
        # transfer list to string
        self.sysbench = '\n'.join(sysbench_stat)
        self.stat = '\n'.join(docker_stat)
