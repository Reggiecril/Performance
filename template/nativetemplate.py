import subprocess
from template import Template


class NativeTemplate(Template):
    def __init__(self,vm_type, test_type,time):
        super(NativeTemplate, self).__init__(vm_type, test_type,time)

    def run_sysbench_vir(self, sys_cmd, vir_stat):
        # run sysbench to test
        p1 = subprocess.Popen(sys_cmd, shell=True,
                              stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        # returncode of p1, if return is None means subprocess is running,if returncode is 0 means subprocess is finised
        returncode = p1.poll()
        sysbench_stat, docker_stat = list(), list()
        # during excuting, get information of p1
        while returncode is None:
            # get sysbench data
            sysbench_line = p1.stdout.readline().strip()
            returncode = p1.poll()
            if sysbench_line == "Threads started!":
                break
        subprocess.call(vir_stat,shell=True)
        while returncode is None:
            # get sysbench data
            sysbench_stat = p1.stdout.readlines()
            returncode = p1.poll()
        subprocess.call('killall -9 pidstat', shell=True)

        # transfer list to string
        self.sysbench += '\n'.join(sysbench_stat)