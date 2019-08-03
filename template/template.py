import ConfigParser
import os

from tool.property import Property


class Template(object):
    def __init__(self, vm_type, test_type):
        self.test_type = test_type
        self.vm_type=vm_type
        #get sysbench and virtual command
        p = Property(vm_type, test_type)
        self.sys_cmd = p.sys_cmd()
        self.vir_stat = p.vir_stat()
        # get the output
        self.sysbench = ""
        self.stat = ""
        # get Property
        self.config_raw = self.read_property("../property.ini")
        self.default = self.config_raw.defaults()
        # init virtual variable
        self.vir_r, self.vir_b, self.vir_swpd, self.vir_free, self.vir_inact, self.vir_active, self.vir_si, self.vir_so, self.vir_bi, self.vir_bo, self.vir_in, self.vir_cs, self.vir_us, self.vir_sy, self.vir_id, self.vir_wa, self.vir_st = list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list(), list()

    # read property
    def read_property(self, test_cfg):
        config_raw = ConfigParser.RawConfigParser()
        config_raw.read(test_cfg)
        return config_raw

    def run(self):
        if self.test_type == 'fileio':
            self.fileio_prepared()
            self.run_sysbench_vir(self.sys_cmd, self.vir_stat)
            self.fileio_clean()
        else:
            self.run_sysbench_vir(self.sys_cmd, self.vir_stat)

    def fileio_prepared(self):
        default = self.config_raw.defaults()
        test = self.get_test(self.test_type)
        parameter = self.get_command(self.get_vm_option_list(self.config_raw.options("Parameter")), "Parameter")
        if self.vm_type:
            cmd = default['sys_name'] + ' ' + self.test_type + ' ' + test + ' ' + parameter + ' prepared'
        else:
            cmd = default['docker_run'] + ' ' + default['docker_image'] + ' ' + default['sys_name'] + ' ' + self.test_type + ' ' + test + ' ' + parameter + ' prepared'

        os.system(cmd)

    def fileio_clean(self):
        default = self.config_raw.defaults()
        test = self.get_test(self.test_type)
        parameter = self.get_command(self.get_vm_option_list(self.config_raw.options("Parameter")), "Parameter")
        if self.vm_type:
            cmd = default['sys_name'] + ' ' + self.test_type + ' ' + test + ' ' + parameter + ' prepared'
        else:
            cmd = default['docker_run'] + ' ' + default['docker_image'] + ' ' + default[
                'sys_name'] + ' ' + self.test_type + ' ' + test + ' ' + parameter + ' prepared'

        os.system(cmd)

    def run_sysbench_vir(self, sys_cmd, vir_stat):
        pass

    # get VM section parameter
    def get_command(self, parameter, string):
        cmd = ''
        for i in parameter:
            cmd += '--' + i + '='
            cmd += self.config_raw.get(string, i) + ' '
        return cmd

    def get_vm_option_list(self, option):
        for i in self.default.keys():
            if i in option:
                option.remove(i)
        return option

    def get_test(self, test_type):
        if test_type != 'cpu' and test_type != 'memory' and test_type != 'threads' and test_type != 'fileio':
            print "Try cpu,memory,threads,memory..."
            os._exit(0)
        cmd = self.get_command(self.get_vm_option_list(self.config_raw.options(test_type)), test_type)
        return cmd
