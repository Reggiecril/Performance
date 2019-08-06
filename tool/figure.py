import matplotlib
matplotlib.use('Agg')
import errno
import os
import matplotlib.pyplot as plt

class Figure(object):
    def __init__(self,time,test_type,vm_or_sys):
        plt.figure(1)
        # image size
        self.time=time
        self.test_type=test_type
        self.vm_or_sys=vm_or_sys

    ######################## Line Figure ########################
    # for each list have to have
    # [label_name,first data list,second data list, color]
    # def one_line_figure(self, role, xlabel, ylabel, file_name):
    #     plt.plot(role[1], role[2], color=role[3], linestyle="--", marker=".", linewidth=1.0, label=role[0])
    #     plt.xlabel(xlabel)
    #     plt.ylabel(ylabel)
    #     plt.legend(loc='upper right')
    #     path = '../figure/' + self.time + '/' + self.test_type + '/'+self.vm_or_sys+'/' + file_name + '.png'
    #     self.check_path(path)
    #     plt.savefig(path)

    # two parametres are list
    # for each list have to have
    # [first data list,second data list]
    def two_line_figure(self, x_coor, vm_list, docker_list, xlabel, ylabel, file_name):
        plt.plot(x_coor, vm_list, color="#0066CC", linestyle="--", marker=".", linewidth=1.0, label="VM")
        plt.plot(x_coor, docker_list, color="#CC0033", linestyle="--", marker="*", linewidth=1.0, label="Docker")
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(loc='upper right')
        plt.show()
        # path='../figure/'+self.time+'/'+self.test_type+'/'+file_name+'.png'
        # self.check_path(path)
        # plt.savefig(path)

    # for each list have to have
    # [label_name,first data list,second data list, color]
    # when have mulitiple figure needs, first need package list to one parent_list
    # like [[label_name,first data list,second data list, color],
    # [label_name,first data list,second data list, color],
    # [label_name,first data list,second data list, color]]
    # def multi_line_figure(self, multi_role, xlabel, ylabel, file_name):
    #     for role in multi_role:
    #         plt.plot(role[1], role[2], color=role[3], linestyle="--", marker=".", linewidth=1.0, label=role[0])
    #     plt.xlabel(xlabel)
    #     plt.ylabel(ylabel)
    #     plt.legend(loc='upper right')
    #     path = '../figure/' + self.time + '/' + self.test_type + '/'+self.vm_or_sys+'/' + file_name+'.png'
    #     self.check_path(path)
    #     plt.savefig(path)

    ######################## Bar Figure ########################
    def bar_figure(self, vm_field, docker_field,file_name):
        a=plt.bar(range(2), [float(vm_field), float(docker_field)],width = 0.35, align='center', tick_label=['vm', 'docker'])
        self.autolabel(a)
        plt.show()
        # path = '../figure/' + self.time + '/' + self.test_type + '/' + file_name+'.png'
        # self.check_path(path)
        # plt.savefig(path)

    def autolabel(self,rects):
        for rect in rects:
            height = rect.get_height()
            plt.text(rect.get_x() + rect.get_width() / 2. - 0.1,  1.01*height, '%s' % float(height))
    def check_path(self,filename):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise