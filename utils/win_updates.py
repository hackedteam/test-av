import subprocess
import ConfigParser
import sys

'''
TODO:
 - find virtual machines
 - for each vm:
   * startup virtual machines
   * send cmd
   * delete current snapshot
   * save new snapshot as current
   * shutdown vm
'''

class Config:
    """ Manage a config file with vm
    """
    def __init__(self, filename):
        self.filename = filename
        self.config = ConfigParser.ConfigParser()
        self.config.read(self.filename)
        self.vsPath = self.config.get('vmware','path')
        
        '''
        self.vsUrl = self.config.get('vmware','host')
        self.vsUser = self.config.get('vmware','user')
        self.vsPass = self.config.get('vmware','passwd')
        '''
        
    def getVms(self):
        vms = self.config.get('vmware','machines')
        return vms.split(",")

    def getVmxPath(self, vm):
        vmx = self.config.get(vm, 'label')
        return vmx


class Operator:
    """ Operator Class
    Sends primitive commands to vSphere via vmrun utility
    """
    
    def __init__(self, vmx, path):
        self.vmrunPath=path
        self.vsUrl="https://vcenter5.hackingteam.local/sdk"
        self.vsUser="avtest"
        self.vsPass="Av!Auto123"
        self.vmUser="avtest"
        self.vmPass="avtest"
        self.vmx=vmx


	def startup(self):
	    """Checking for interactive startup
	    """
        cmd = subprocess.Popen([self.vmrunPath,
								"-h", self.vsUrl,
								"-u", self.vsUser,
								"-p", self.vsPass,
								"start", self.vmx ])
		
	
	def shutdown(self):
		cmd = subprocess.Popen([self.vmrunPath,
								"-h", self.vsUrl,
								"-u", self.vsUser,
								"-p", self.vsPass,
								"stop", self.vmx ])



    def deleteSnapshot(self, snapshot):
        cmd = subprocess.Popen([self.vmrunPath,
								"-h", self.vsUrl,
								"-u", self.vsUser,
								"-p", self.vsPass,
								"deleteSnapshot", self.vmx,
								snapshot ])
	
	
	def takeSnapshot(self, snapshot):
	    cmd = subprocess.Popen([self.vmrunPath,
	                            "-h", self.vsUrl,
	                            "-u", self.vsUser,
	                            "-p", self.vsPass,
    							"snapshot", self.vmx,
    					        snapshot ])
        
        
    
    def executeCmd(self, script):
        cmd = subprocess.Popen([vmrunPath,
    			                "-h", self.vsUrl,
    							"-u", self.vsUser, "-p", self.vsPass,
    							"-gu", self.vmUser, "-gp", self.vmPass,
    							"runProgramInGuest", self.vmx,
    					        script ])
        



class Commander:    
    """
    Commander Class
    Sends operations to Operator for one Virtual Machine specified as input
    """
    
    def __init__(self, vm, path):
        self.vm = vm
        self.path = path
        
    def startVm(self):
        Operator(self.vm, self.path).startup()
        
    def stopVm(self):
        Operator(self.vm, self.path).shutdown()
    
    def sendUpgrade(self, cmd):
        Operator(self.vm, self.path).executeCmd(cmd)

    def refreshSnapshot(self, snapshot):
        Operator(self.vm, self.path).deleteSnapshot(snapshot)
        Operator(self.vm, self.path).takeSnapshot(snapshot)

        

if __name__ == "__main__":
    
    vmware_config_file="conf/vmware.conf"
    cmd = "C:/script/win_update.bat"
    snapshot="current"
    c = Config(vmware_config_file)
    vms = c.getVms()
    
    for vm in vms:
        cmd = Commander(c.getVmxPath(vm), c.vsPath)
        
        sys.stdout.write("Starting Virtual Machine %s" % vm)
        cmd.startVm()
        
        sys.stdout.write("Starting Upgrade")
        cmd.sendUpgrade(cmd)
        
        sys.stdout.write("Refreshing Snapshot")
        cmd.refreshSnapshot(snapshot)
        
        sys.stdout.write("Stopping Virtual Machine %s" % vm)
        cmd.stopVm()
        
        sys.stdout.write("Done.")
    sys.stdout.write("End")    