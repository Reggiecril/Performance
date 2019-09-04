from template.dockertemplate import Dockertemplate
from module import Module
class Docker(Module):
    def __init__(self, time):
        super(Docker, self).__init__(time)
    def run(self, test_type):

        t = Dockertemplate('docker', test_type,self.now_time)
        t.run()
        sysbench_path="./file/docker/" + test_type + '/' +'sysbench/'+ self.now_time + ".txt"
        self.check_path(sysbench_path)
        f = open(sysbench_path, "w")
        f.write(t.sysbench)

    def process(self, test_type):
        self.check_test_type(test_type)
        self.run(test_type)

