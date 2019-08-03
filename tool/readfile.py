import re


class ReadFile:
    def __init__(self, type, filename):
        self.filename = filename
        self.type = type

    def sysbench_data(self, line):
        li = list()
        b = re.match(r"(.*)\[([^\[\]]*)\](.*)", line, re.I | re.M)
        li.append(b.group(2).strip().replace('s',''))
        line_spilt = line.split(' ')
        for i in line_spilt:
            if self.isnumber(i):
                li.append(i)
        return li

    def vm_data(self, line):
        l = line.split(" ")
        count = 0
        while count < len(l):
            if l[count] == " " or l[count] == "":
                l.pop(count)
            else:
                count += 1
        return l

    def docker_data(self, line):
        dic = eval(line[line.index('{'):])
        return dic

    def read_file(self):
        file = open(self.filename, "r")
        list_sysbench, list_virstat = list(), list()

        for line in file.readlines():
            if line[0] == '[' and ']' in line:
                line = line.strip()
                list_sysbench.append(self.sysbench_data(line))
            if self.type:
                if line.replace(" ", "").strip().isdigit():
                    list_virstat.append(self.vm_data(line.strip()))
            else:
                if '{' in line:
                    dic = self.docker_data(line.strip())
                    list_virstat.append(dic)
        return list_sysbench, list_virstat

    def isnumber(self,aString):
        try:
            float(aString)
            return True
        except:
            return False
