# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.
import os

from lib.common.abstracts import Package
from lib.api.process import Process

class Av(Package):
    """AntiVirus analysis package."""
    def __init__(self):
        self._agent_dir = "\%APPDATA\%\\.."
    
    def list_dir(self):
        dirs = os.listdir(self._agent_dir)
        return dir

    def start(self, path):
        
        before = self.list_dir()
        print before
        
        p = Process()

        if "arguments" in self.options:
            p.execute(path=path, args=self.options["arguments"], suspended=True)
        else:
            p.execute(path=path, suspended=True)
        after = self.list_dir()
        
        print after
        
        return p.pid

    def check(self):
        return True

    def finish(self):
        return True
