import subprocess
from template import Template


class Dockertemplate(Template):
    def __init__(self, vm_type, test_type):
        super(Dockertemplate, self).__init__(vm_type, test_type)

    def run_sysbench_vir(self, sys_cmd, vir_stat):
        print sys_cmd
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
                # run docker stats
        count = 0
        while returncode is None:
            # get sysbench data
            sysbench_line = p1.stdout.readline().strip()
            sysbench_stat.append(sysbench_line)
            print sysbench_line
            if count == 0:
                p2 = subprocess.Popen(vir_stat, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                p2.stdout.readline()
                p2.stdout.readline()
                p2.stdout.readline()
                count += 1
            # check
            if sysbench_line.strip() == '':
                continue
            # get docker data
            if sysbench_line[0] == '[':
                docker_line = p2.stdout.readline()
                docker_stat.append(docker_line)
                print docker_line
            else:
                p2.kill()
                break
            returncode = p1.poll()
        while returncode is None:
            # get sysbench data
            sysbench_line = p1.stdout.readline().strip()
            sysbench_stat.append(sysbench_line)
            print sysbench_line
            returncode = p1.poll()
        # transfer list to string
        self.sysbench = '\n'.join(sysbench_stat)
        self.stat = '\n'.join(docker_stat)
