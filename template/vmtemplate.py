import os
import datetime
import subprocess

from template import Template


class VMTemplate(Template):
    def __init__(self,DB_cmd, sys_cmd, vir_stat, clean_cmd):
        super(VMTemplate, self).__init__(DB_cmd, sys_cmd, vir_stat, clean_cmd)
    def run_sysbench_vir(self, sys_cmd,vir_stat):
        # run sysbench to test
        p1 = subprocess.Popen(sys_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # returncode of p1, if return is None means subprocess is running,if returncode is 0 means subprocess is finised
        returncode = p1.poll()
        sysbench = list()
        self.run_vir(vir_stat)
        # during excuting, get information of p1
        while returncode is None:
            line = p1.stdout.readline().strip()
            sysbench.append(line)
            returncode = p1.poll()
            print line
        self.sysbench = '\n'.join(sysbench)

    def run_vir(self, vir_stat):
        # run vmstat per 5s to get state of file
        self.stat = subprocess.check_output(vir_stat.split(" "))
