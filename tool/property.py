import ConfigParser
import errno
import os


class Property:
    def __init__(self, module_type, test_type, time):
        self.module_type = module_type
        self.config_raw = self.read_property("./property.ini")
        self.default = self.config_raw.defaults()
        # Parameter Section
        self.parameter = self.get_command(self.get_vm_option_list(self.config_raw.options("Parameter")), "Parameter")
        # test type section
        self.test = self.get_test(test_type)
        self.test_type = test_type
        self.time = time

    def read_property(self, test_cfg):
        config_raw = ConfigParser.RawConfigParser()
        config_raw.read(test_cfg)
        return config_raw

    # if type ==True ==> VM
    # else if type == False ==> Docker
    def sys_cmd(self):
        cmd = ''
        if self.module_type == 'vm' or self.module_type == 'native':
            cmd = self.default['sys_name'] + ' ' + self.test + ' ' + self.parameter + ' run'
        elif self.module_type == 'docker':
            cmd = self.default['docker_run'] + ' ' + self.default['docker_image'] + ' ' + self.default[
                'sys_name'] + ' ' + self.test + ' ' + self.parameter + ' run'
        return cmd

    # if type ==True ==> VM
    # else if type == False ==> Docker
    def vir_stat(self):
        report_interval = self.config_raw.getint("Parameter", "report-interval")

        if self.module_type == 'vm':
            file_path = './file/vm/' + self.test_type + '/pidstat/' + self.time + '/'
            self.check_path(file_path)
            cmd = self.default[
                      'vm_name'] + ' ' + str(
                report_interval) + ' >' + file_path + ' &'
        elif self.module_type == 'docker':
            file_path = './file/docker/' + self.test_type + '/pidstat/' + self.time+'/'
            self.check_path(file_path)
            cmd = self.default['docker_run'] + ' ' + self.default['docker_image'] + ' ' + self.default[
                'vm_name'] + ' ' + str(
                report_interval) + ' >' + file_path + ' &'
        else:
            file_path = './file/native/' + self.test_type + '/pidstat/' + self.time + '/'
            self.check_path(file_path)
            cmd = self.default[
                      'vm_name'] + ' ' + str(
                report_interval) + ' >' + file_path + ' &'
        return cmd

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
        cmd = self.get_command(self.get_vm_option_list(self.config_raw.options(test_type)), test_type)
        return test_type + ' ' + cmd

    def check_path(self, filename):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
