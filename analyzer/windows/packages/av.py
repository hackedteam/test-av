# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.
from lib.common.abstracts import Package
from lib.api.process import Process

import os
import wmi


class Av(Package):
    """AntiVirus analysis package."""
    def __init__(self):
        self._agent_dir = "%APPDATA%\\.."
        self.c = wmi.WMI()
        self.process_watcher = self.c.Win32_Process.watch_for("creation")
    
    def list_dir(self):
        dirs = os.listdir(self._agent_dir)
        return dir

    def start(self, path):
                
        p = Process()

        if "arguments" in self.options:
            p.execute(path=path, args=self.options["arguments"], suspended=True)
        else:
            p.execute(path=path, suspended=True)
        
        print("sleeping for demo windows")
        sleep(15)
        return p.pid

    def check(self):
        proc = self.process_watcher()
        if proc:
            return True 
            #proc.Caption
        return False

    def finish(self):
        return True
