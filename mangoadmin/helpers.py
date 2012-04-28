from fabric.api import env
from fabric.api import run, sudo
from fabric.api import settings
from fabric.api import hide

class FabricSupport:
    def __init__ (self):
        pass

    def _cmd(self, host, port, command):
        with settings(
                      hide('warnings', 'running', 'stdout', 'stderr'),
                      warn_only=True):
            env.host_string = "%s:%s" % (host, port)
            _cmd(command)
    def run(self, host, port, command)
        self._cmd(host, port, command)

    def sudo(self, host, port, command)
        self._cmd(host, port, command)

fabcmd = FabricSupport()
