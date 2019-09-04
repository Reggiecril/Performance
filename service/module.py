import ConfigParser
import errno
import os


class Module(object):
    def __init__(self, time):
        # (%Y-%m-%d %H:%M:%S%f)
        self.now_time = time
        self.config_raw = self.read_property("../property.ini")
    def run(self, test_type):
        pass

    def process(self, test_type):
        pass

    def check_test_type(self, test_type):
        if test_type != 'cpu' and test_type != 'memory' and test_type != 'fileio' and test_type != 'threads':
            print "Please enter one of \'cpu\' , \'memory\' , \'fileio\' ,\'threads\'"
            os._exit(0)
    def read_property(self, test_cfg):
        config_raw = ConfigParser.RawConfigParser()
        config_raw.read(test_cfg)
        return config_raw
    def check_path(self, filename):
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

