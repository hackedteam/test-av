import argparse
import sys
from time import sleep

from lib.config import Config
from lib.command import Command			

class WinUpdate:
	def __init__(self):
		# init stuff
		self.config_file = "c:/test-av/conf/vmware.conf"
		self.conf = Config(self.config_file)
		self.cmd = Command(self.conf.path, self.conf.host, self.conf.user, self.conf.passwd)
		
		# full paths of script neede for update
		self.cscriptPath="c:/windows/system32/cscript.exe"
		self.netENScript="c:/Users/avtest/Desktop/EnableIF.bat"
		self.netDISScript="c:/Users/avtest/Desktop/DisableIF.bat"
		self.scriptPath="c:/Users/avtest/Desktop/WUA_SearchDownloadInstall.vbs"
		

	def doUpdate(self, vmx):
		if vmx == 'all':
			#update all vms
			vms = self.conf.getMachines()
			
			sys.stdout.write("[*] Starting all guests.\n")
			for vm in vms:
				self.cmd.startup(self.conf.getVmx(vm))
				sleep(5)
				
			sys.stdout.write("[*] Enabling Networking on guests.\n")
			for vm in vms:
				self.cmd.executeCmd(self.conf.getVmx(vm), self.netENScript)

			sys.stdout.write("[*] Updating operatings system on guests.\n")
			for vm in vms:
				self.cmd.executeCmd(self.conf.getVmx(vm), self.cscriptPath, self.netDISScript)
		
		else:
			sys.stdout.write("[*] Starting %s.\n" % vmx)
			self.cmd.startup(self.conf.getVmx(vmx))
			sleep(60)
			sys.stdout.write("[*] Enabling Networking on %s.\n" % vmx)
			self.cmd.executeCmd(self.conf.getVmx(vmx), self.netENScript)
			sleep(10)
			sys.stdout.write("[*] Updating operatings system on %s.\n" % vmx)
			self.cmd.executeCmd(self.conf.getVmx(vmx), self.cscriptPath, self.scriptPath)
			
	
	def doReboot(self, vmx):
		if vmx == "all":
			vms = self.conf.getMachines()
			sys.stdout.write("[*] Disabling network on guests.\n")
			for vm in vms:
				self.cmd.executeCmd(self.conf.getVmx(vm), self.netDISScript)
				sleep(5)
			sys.stdout.write("[*] Rebooting guests.\n")
			for vm in vms:
				self.cmd.reboot(self.conf.getVmx(vm))
				sleep(5)	
		else:
			vm = self.conf.getVmx(vmx)
			sys.stdout.write("[*] Disabling network on %s.\n" % vmx)
			self.cmd.executeCmd(vm, self.netDISScript)
			sleep(20)
			sys.stdout.write("[*] Rebooting %s.\n" % vmx)
			self.cmd.reboot(vm)


	def refreshShot(self, vmx):
		if vmx == "all":
			sys.stdout.write("[*] Refresh snapshots on guests.\n")
			for vm in vms:
				self.cmd.refreshSnapshot(self.conf.getVmx(vm))
				sleep(10)
		else:
			sys.stdout.write("[*] Refresh snapshot of %s" % vmx)
			self.cmd.refreshSnapshot(self.conf.getVmx(vmx))
	
'''
MAIN
	
	parser = argparse.ArgumentParser(description='VMs updater script')
	parser.add_argument('op', metavar='operation', type=str,
						help='operation to perform (start,reboot,refresh)')
	args = parser.parse_args()
	
	if args.op == "start":
		""" Stage 1:
		For each VM startup and launch update script
		"""
		sys.stdout.write('[*] Startin Virtual machines\n\n')
		for vm in vms:

			sys.stdout.write("[*] Updating %s\n" % vm)	
			vmx = conf.getVmx(vm)
			cmd = Command(vmx, exe)
			cmd.revertSnapshot("current")
			sleep(10)
			cmd.startup()
			sleep(40)
			cmd.executeCmd(netENScript,None)
			sleep(10)
			cmd.update()

	elif args.op == "reboot":
		""" Stage 2:
		Reboot for updates
		"""
		sys.stdout.write('[*] Performing reboot')
		for vm in vms:
			vmx = conf.getVmx(vm)
			cmd = Command(vmx, exe)
			#cmd.shutdown()
			#cmd.startup()
			cmd.reboot()
			sleep(5)
				
	elif args.op == "refresh":
		""" Stage 3:
		Refresh all VMs' snapshots and shut them down (remember reboot to apply all updates!!)
		"""
		sys.stdout.write('[*] Refreshing vms snapshots')
		for vm in vms:
			vmx = conf.getVmx(vm)
			cmd = Command(vmx, exe)
			cmd.executeCmd(netDISScript,None)
			#cmd.refreshSnapshot("current")
			sleep(30)
			cmd.shutdown()
			sleep(1)
	
	else:
		print '[*] no action will be performed'
		

'''	
wu = WinUpdate()
wu.doUpdate('norman')