from datetime import datetime

from service.docker import Docker
from service.virtualmachine import Virtaulmachine
from tool.remote_vm import RemoteVM

if __name__ == '__main__':
    time = datetime.now().strftime("%Y%m%d%H%M%S%f")
    # r = RemoteVM(time)
    # r.update_property()
    # r.execute()
    d = Docker(time)
    d.process("cpu")
    d.process("memory")
    d.process("fileio")
    d.process("threads")
    v=Virtaulmachine(time)
    v.process("cpu")
    v.process("memory")
    v.process("fileio")
    v.process("threads")