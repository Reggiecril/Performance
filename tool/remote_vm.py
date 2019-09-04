import ConfigParser
import os

import paramiko
from stat import S_ISDIR as isdir

class RemoteVM(object):
    def __init__(self,time):
        self.time=time
        config_raw = self.read_property("./property.ini")
        self.host = config_raw.get('Remote', 'host')
        self.user = config_raw.get('Remote', 'user')
        self.password = config_raw.get('Remote', 'password')
        self.port = config_raw.get('Remote', 'port')
    def update_property(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(self.host, username=self.user, password=self.password, port=int(self.port))
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        sftp.put('./property.ini','/home/Performance/property.ini')
        client.close()
    def execute(self):
        client = paramiko.SSHClient()
        client.load_system_host_keys()
        client.connect(self.host, username=self.user, password=self.password, port=int(self.port))
        stdin, stdout, stderr = client.exec_command('cd /home/Performance  && python excute_vm.py '+self.time)
        print stdout.readlines()
        sftp = paramiko.SFTPClient.from_transport(client.get_transport())
        self.down_from_remote(sftp,'/home/Performance/file/vm','./file/vm')
        client.exec_command('cd /home/Performance  && rm -rf file')
        client.close()

    def down_from_remote(self,sftp, remote_dir_name, local_dir_name):
        remote_file = sftp.stat(remote_dir_name)
        if isdir(remote_file.st_mode):
            self.check_local_dir(local_dir_name)
            print('Downloading:' + remote_dir_name)
            for remote_file_name in sftp.listdir(remote_dir_name):
                sub_remote = os.path.join(remote_dir_name, remote_file_name)
                sub_remote = sub_remote.replace('\\', '/')
                sub_local = os.path.join(local_dir_name, remote_file_name)
                sub_local = sub_local.replace('\\', '/')
                self.down_from_remote(sftp, sub_remote, sub_local)
        else:
            print('Downloading:' + remote_dir_name)
            sftp.get(remote_dir_name, local_dir_name)

    def check_local_dir(self,local_dir_name):
        if not os.path.exists(local_dir_name):
            os.makedirs(local_dir_name)

    def read_property(self, test_cfg):
        config_raw = ConfigParser.RawConfigParser()
        config_raw.read(test_cfg)
        return config_raw
