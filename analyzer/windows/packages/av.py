# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

from lib.common.abstracts import Package
from lib.api.process import Process

import wmi
import pythoncom
import threading


class Av(Package):
    """Av analysis package."""

	
    def start(self, path):
        #print globals()
        #print self.options["machine"]
		
        p = Process()
		
        if "arguments" in self.options:
            p.execute(path=path, args=self.options["arguments"], suspended=False)
        else:
            p.execute(path=path, suspended=False)
			

        return p.pid

    def check(self):
        return True

    def finish(self):
        return True
