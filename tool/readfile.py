import re


class ReadFile:
    def __init__(self, filename):
        self.filename = filename

    def sysbench_data(self, line):
        li = list()
        b = re.match(r"(.*)\[([^\[\]]*)\](.*)", line, re.I | re.M)
        li.append(b.group(2).strip().replace('s', ''))
        line_spilt = line.split(' ')
        for i in line_spilt:
            i=i.replace('/s','')
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

    def read_file(self):
        file = open(self.filename, "r")
        list_sysbench, list_virstat,dict_statistics = list(), list(), dict()
        val = ''
        for line in file.readlines():
            if line.strip() == '':
                continue
            if line[0] == '[' and ']' in line:
                line = line.strip()
                list_sysbench.append(self.sysbench_data(line))
                continue
            if line.replace(" ", "").strip().isdigit():
                list_virstat.append(self.vm_data(line.strip()))
                continue
            sub_sp = line.split(':')
            if len(sub_sp)<2:
                continue
            if sub_sp[1].strip() == '':
                val = sub_sp[0].replace(' ', '_').replace('_(ms)', '').strip()
                dict_statistics[val] = dict()
                continue
            if val=='':
                dict_statistics[sub_sp[0].replace(' ', '_').strip()]=sub_sp[1].strip()
                continue
            dict_statistics[val][sub_sp[0].strip().replace(' ', '_')] = sub_sp[1].strip()
        return list_sysbench, list_virstat,dict_statistics
    def isnumber(self, aString):
        try:
            float(aString)
            return True
        except:
            return False
