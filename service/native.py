from module import Module
from template.nativetemplate import NativeTemplate
class Native(Module):
    def __init__(self, time):
        super(Native, self).__init__(time)

    def run(self, test_type):
        t = NativeTemplate('native', test_type,self.now_time)
        t.run()
        sysbench_path="./file/native/" + test_type + '/' +'sysbench/'+ self.now_time + ".txt"
        self.check_path(sysbench_path)
        f = open(sysbench_path, "w")
        f.write(t.sysbench)

    def process(self, test_type):
        self.check_test_type(test_type)
        self.run(test_type)
        # list_sysbench,dict_statistics = ReadFile("./file/vm/" + test_type + '/'+'sysbench/' + self.now_time + ".txt").read_sysbench_file()
        # list_virstat=ReadFile("./file/vm/" + test_type + '/'+'pidstat/'+ self.now_time + ".log").read_pidstat_file()
        # print list_sysbench,dict_statistics
        # print list_virstat
        # self.get_sys_data(list_sysbench,test_type)
        # self.get_vir_data(list_virstat)
        # self.get_statistics_data(dict_statistics, test_type)