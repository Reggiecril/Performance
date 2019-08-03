import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
class LineFigure:
    def __init__(self):
        # image size
        plt.figure(1)

    # for each list have to have
    # [label_name,first data list,second data list, color]
    def one_line(self, role,xlabel,ylabel,name):
        plt.plot(role[1], role[2], color=role[3], linestyle="--", marker=".", linewidth=1.0,label=role[0])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(loc='upper right')
        plt.savefig(name)
    # two parametres are list
    # for each list have to have
    # [label_name,first data list,second data list, color]
    def two_line(self, first_role, second_role,xlabel,ylabel,name):
        plt.plot(first_role[1], first_role[2], color=first_role[3], linestyle="--", marker=".", linewidth=1.0,label=first_role[0])
        plt.plot(second_role[1], second_role[2], color=second_role[3], linestyle="--", marker=".", linewidth=1.0,label=second_role[0])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(loc='upper right')
        plt.savefig(name)
    # for each list have to have
    # [label_name,first data list,second data list, color]
    # when have mulitiple figure needs, first need package list to one parent_list
    # like [[label_name,first data list,second data list, color],
    # [label_name,first data list,second data list, color],
    # [label_name,first data list,second data list, color]]
    def multi_line(self, multi_role,xlabel,ylabel,name):
        for role in multi_role:
            plt.plot(role[1], role[2], color=role[3], linestyle="--", marker=".", linewidth=1.0,label=role[0])
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.legend(loc='upper right')
        plt.savefig(name)


