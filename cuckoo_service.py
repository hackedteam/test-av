import subprocess
import traceback
import os
import sys

import win32serviceutil
import win32service
import win32event


class testLauncher(win32serviceutil.ServiceFramework):

    _svc_name_ = 'AVTEST-CUCKOO'
    _svc_display_name_ = 'AV TESTER CUCKOO'
    _svc_description_ = "NA"
	
    def __init__(self, *args):
        win32serviceutil.ServiceFramework.__init__(self, *args)
        self.log('init')
        self.runflag = True
        self.stop_event = win32event.CreateEvent(None, 0, 0, None)

    def log(self, msg):
        import servicemanager
        servicemanager.LogInfoMsg(str(msg))

    def sleep(self, sec):
        win32api.Sleep(sec*1000, True)

    def SvcDoRun(self):
        self.ReportServiceStatus(win32service.SERVICE_START_PENDING)
        try:
            self.ReportServiceStatus(win32service.SERVICE_RUNNING)
            self.log('start')
            sys.stdout.write("starting")
            self.start()
            while self.runflag == True:
                pass
            self.log('wait')
            win32event.WaitForSingleObject(self.stop_event, win32event.INFINITE)
            self.log('done')
        except Exception, x:
            self.log('Exception : %s' % x)
            self.SvcStop()

    def SvcStop(self):
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        self.log('stopping')
        self.stop()
        self.log('stopped')
        win32event.SetEvent(self.stop_event)
        self.ReportServiceStatus(win32service.SERVICE_STOPPED)

    def start(self):
        sys.stdout.write("opening")
        pyPath   = "c:/Python27/python.exe"
        cuckooPath = "c:/test-av/cuckoo.py"
        os.chdir("c:/test-av/")
        proc = subprocess.call([pyPath,cuckooPath],
                                stdin = subprocess.PIPE,
                                stdout = subprocess.PIPE)
			
    def stop(self): 
        self.runflag = False
        
        
if __name__ == "__main__":
    win32serviceutil.HandleCommandLine(testLauncher)
