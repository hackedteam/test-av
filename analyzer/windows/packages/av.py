# Copyright (C) 2010-2012 Cuckoo Sandbox Developers.
# This file is part of Cuckoo Sandbox - http://www.cuckoosandbox.org
# See the file 'docs/LICENSE' for copying permission.

import threading
import pythoncom
import wmi

from lib.common.abstracts import Package
from lib.api.process import Process

class Avira( threading.Thread ):
    def __init__(self):
      threading.Thread.__init__(self)

    def run(self):
      #c = wmi.WMI()
      pythoncom.CoInitialize()

      try:
        new_proc = False
        c = wmi.WMI()
        process_watcher = c.Win32_Process.watch_for("creation")

        while True:
          new_process = process_watcher()
          
          if new_process.Caption == 'guardgui.exe':
            print result = 'malware found, AV process detected'
            break
          

      finally:
        pythoncom.CoUninitialize()


class Av(Package):
    """EXE analysis package."""

	def test_avira(self):
	
	
    def start(self, path):
        p = Process()

        if "arguments" in self.options:
            p.execute(path=path, args=self.options["arguments"], suspended=True)
        else:
            p.execute(path=path, suspended=True)
			
		if self.options["machine"] == "avira":
			print "im on avira bro!"

        return p.pid

    def check(self):
        return True

    def finish(self):
        return True
