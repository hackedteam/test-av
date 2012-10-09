import subprocess
import sys
import os

class Command:
	def __init__(self, path, host, user, passwd):
		self.path = path
		self.host = host
		self.user = user
		self.passwd = passwd
	
	def startup(self, vmx):
		sys.stdout.write("\r\nStartup %s!\r\n" % vmx)
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"start", vmx])
	
	def shutdown(self, vmx):
		sys.stdout.write("\r\nShutdown %s!\r\n" % vmx)
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"stop", vmx])

	def reboot(self, vmx):
		sys.stdout.write("\r\nRebooting %s!\r\n" % vmx)
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"reset", self.vmx, "soft"])

	def suspend(self):
		sys.stdout.write("\r\nSuspending %s!\r\n" % vmx)
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"suspend", self.vmx, "soft"])
		
	def executeCmd(self, cmd, script=None):
		sys.stdout.write("Executing %s %s.\n" % (cmd, script))
		if script is not None:
			subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"-gu", "avtest", "-gp", "avtest",
						"runProgramInGuest", self.vmx, cmd, script, ">","c:/Users/avtest/Documents/update.log"])			
		else:
			subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"-gu", "avtest", "-gp", "avtest",
						"runProgramInGuest", self.vmx, cmd,">","c:/Users/avtest/Documents/update.log"])
	
	
	def update(self):
		cscriptPath="c:/windows/system32/cscript.exe"
		scriptPath="z:/WUA_SearchDownloadInstall.vbs"	
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"-gu", "avtest", "-gp", "avtest",
						"runProgramInGuest", self.vmx, "c:/windows/system32/cscript.exe","c:/Users/avtest/WUA_SearchDownloadInstall.vbs"])
						
	def refreshSnapshot(self, snapshot):
		sys.stdout.write("Deleting current snapshot.\n")
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"deleteSnapshot", self.vmx, snapshot])
		sys.stdout.write("Creating new current snapshot.\n")
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"snapshot", self.vmx, snapshot])
						
	def revertSnapshot(self, snapshot):
		sys.stdout.write("Reverting to current snapshot.\n")
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"revertToSnapshot", self.vmx, snapshot])
