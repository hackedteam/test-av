import subprocess
import sys
import os

class Command:
	def __init__(self, path, host=None, user=None, passwd=None):
		if not host and not user and not passwd:
			self.path = path
		else:
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
						"reset", vmx, "soft"])

	def suspend(self, vmx):
		sys.stdout.write("\r\nSuspending %s!\r\n" % vmx)
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"suspend", vmx, "soft"])
		
	def executeCmd(self, vmx, cmd, script=None):
		sys.stdout.write("Executing %s %s.\n" % (cmd, script))
		if script is not None:
			subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"-gu", "avtest", "-gp", "avtest",
						"runProgramInGuest", vmx, cmd, script])			
		else:
			subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"-gu", "avtest", "-gp", "avtest",
						"runProgramInGuest", vmx, cmd])
	
	
	def update(self, vmx):
		cscriptPath="c:/windows/system32/cscript.exe"
		scriptPath="z:/WUA_SearchDownloadInstall.vbs"	
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"-gu", "avtest", "-gp", "avtest",
						"runProgramInGuest", vmx, "c:/windows/system32/cscript.exe","c:/Users/avtest/WUA_SearchDownloadInstall.vbs"])
						
	def refreshSnapshot(self, vmx, snapshot):
		sys.stdout.write("Deleting current snapshot.\n")
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"deleteSnapshot", vmx, snapshot])
		sys.stdout.write("Creating new current snapshot.\n")
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"snapshot", vmx, snapshot])
						
	def revertSnapshot(self, vmx, snapshot):
		sys.stdout.write("Reverting to current snapshot.\n")
		subprocess.call([self.path,
						"-h", self.host,
						"-u", self.user, "-p", self.passwd,
						"revertToSnapshot", vmx, snapshot])
