nimport subprocess
import ConfigParser
import sys
from time import sleep

class Config:
	def __init__(self, conf):
		self.conf = ConfigParser.ConfigParser()
		self.file = conf

	def getVmx(self, vm):
		self.conf.read(self.file)
		vmx = self.conf.get(vm, 'label')
		return vmx
    
	def getVmrunPath(self):
		self.conf.read(self.file)
		path = self.conf.get('vmware','path')
		return path
        
	def getMachines(self):
		self.conf.read(self.file)
		vms = self.conf.get('vmware', 'machines').split(",")
		return vms

class Command:
	def __init__(self, vmx, path):
		self.vmx = vmx
		self.path = path
        
	def show(self):
		sys.stdout.write("\r\nshowing all stuff:\nvmx: %s\npath: %s\r\n" % (self.vmx, self.path))
	
	def startup(self):
		subprocess.Popen([self.path,
						"-h", "https://vcenter5.hackingteam.local/sdk",
						"-u", "avtest", "-p", "Av!Auto123",
						"start", self.vmx])
		sys.stdout.write("\r\nStartup %s!\r\n" % vmx)
	
	def shutdown(self):
		subprocess.Popen([self.path,
						"-h", "https://vcenter5.hackingteam.local/sdk",
						"-u", "avtest", "-p", "Av!Auto123",
						"stop", self.vmx])
		sys.stdout.write("\r\nShutdown %s!\r\n" % vmx)
		
	def executeCmd(self, cmd, script):
		sys.stdout.write("Executing %s %s.\n" % (cmd, script))
		subprocess.Popen([self.path,
						"-h", "https://vcenter5.hackingteam.local/sdk",
						"-u", "avtest", "-p", "Av!Auto123",
						"-gu", "avtest", "-gp", "avtest",
						"runProgramInGuest", self.vmx, cmd, script])
						
	def refreshSnapshot(self, snapshot):
		sys.stdout.write("Deleting current snapshot.\n")
		subprocess.Popen([self.path,
						"-h", "https://vcenter5.hackingteam.local/sdk",
						"-u", "avtest", "-p", "Av!Auto123",
						"deleteSnapshot", self.vmx, snapshot])
		sys.stdout.write("Creating new current snapshot.\n")
		subprocess.Popen([self.path,
						"-h", "https://vcenter5.hackingteam.local/sdk",
						"-u", "avtest", "-p", "Av!Auto123",
						"snapshot", self.vmx, snapshot])
						
	def revertSnapshot(self, snapshot):
		sys.stdout.write("Reverting to current snapshot.\n")
		subprocess.Popen([self.path,
						"-h", "https://vcenter5.hackingteam.local/sdk",
						"-u", "avtest", "-p", "Av!Auto123",
						"revertToSnapshot", self.vmx, snapshot])
		

if __name__ == "__main__":
	config_file = "c:/test-av/conf/vmware.conf"
	cscriptPath="c:/windows/system32/cscript.exe"
	scriptPath="c:/script/WUA_SearchDownloadInstall.vbs"
	conf = Config(config_file)
	vms = conf.getMachines()
	exe = conf.getVmrunPath()
	
	for vm in vms:
		#if vm == "gdata" or vm == "kav" or vm == "avira" or vm == "avg":
		#	continue
		sys.stdout.write("Updating %s\n" % vm)	
		vmx = conf.getVmx(vm)
		cmd = Command(vmx, exe)
		cmd.revertSnapshot("current")
		sleep(3)
		cmd.startup()
		sleep(10)
		cmd.executeCmd(cscriptPath,scriptPath)
		sleep(20)
		cmd.refreshSnapshot("current")
		sleep(3)
		cmd.shutdown()
		sleep(1)


