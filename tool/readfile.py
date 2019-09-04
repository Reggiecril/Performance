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
            i = i.replace('/s', '')
            if self.isnumber(i):
                li.append(i)
        return li

    def pidstat_data(self, line):
        l = line.split(" ")
        count = 0
        while count < len(l):
            if l[count] == " " or l[count] == "":
                l.pop(count)
            else:
                count += 1

        return l

    def statistics_data(self, val, line, dict_statistics):
        sub_sp = line.split(':')
        if sub_sp[1].strip() == '':
            val = sub_sp[0].replace(' ', '_').replace('_(ms)', '').strip()
            if not dict_statistics.has_key(val):
                dict_statistics[val] = dict()
            return val, dict_statistics
        # for memory only
        if sub_sp[0] == 'Total operations':
            dict_statistics = self.default_dict_key(dict_statistics, sub_sp[0].replace(' ', '_').strip(), float(
                re.findall("(?<=\\()(.+?)(?=\\))", sub_sp[1].strip())[0].strip().split(' ')[0]))
            return val, dict_statistics
        if '(avg/stddev)' in sub_sp[0]:
            sub_sp[0] = sub_sp[0].split('/')[0].replace('(', '')
        if '/s' in sub_sp[0]:
            sub_sp[0] = sub_sp[0].replace(', MiB/s', '').replace('/s', '')
        if '/' in sub_sp[1]:
            sub_sp[1] = sub_sp[1].split('/')[0]
        sub_sp[1] = sub_sp[1].replace('s', '')
        # dict_statistics[val].setdefault(sub_sp[0].strip().replace(' ', '_'), list())
        # dict_statistics[val][sub_sp[0].strip().replace(' ', '_')].append(float(sub_sp[1].strip()))
        dict_statistics[val]=self.default_dict_key(dict_statistics[val], sub_sp[0].strip().replace(' ', '_'), float(sub_sp[1].strip()))
        return val, dict_statistics

    def default_dict_key(self, dict, key, value):
        if dict.has_key(key):
            dict[key].append(value)
        else:
            dict[key] = list()
            dict[key].append(value)
        return dict

    def read_sysbench_file(self):
        file = open(self.filename, "r")
        list_sysbench, dict_statistics = list(), dict()
        val = ''
        for line in file.readlines():
            if line[0] == '[' and ']' in line:
                line = line.strip()
                list_sysbench.append(self.sysbench_data(line))
                continue
            if ':' in line:
                val, dict_statistics = self.statistics_data(val, line, dict_statistics)
                continue
        return list_sysbench, dict_statistics

    def read_pidstat_file(self):
        list_virstat = list()
        with open(self.filename) as file:
            for line in file:
                line = line.strip()
                line_split = line.split(' ')
                if line_split[-1] == 'sysbench':
                    one_sysbench_line = list()
                    for i in line_split:
                        if self.isnumber(i):
                            one_sysbench_line.append(float(i))
                    if self.filename.split('/')[1] != 'vm':
                        one_sysbench_line=one_sysbench_line[2:-1]
                        one_sysbench_line.pop(3)
                    else:
                        one_sysbench_line=one_sysbench_line[3:]

                    list_virstat.append(one_sysbench_line)
        return list_virstat

    def isnumber(self, aString):
        try:
            float(aString)
            return True
        except:
            return False
