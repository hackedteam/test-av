import ConfigParser

class Config:
	def __init__(self, conf):
		self.conf = ConfigParser.ConfigParser()
		self.file = conf
		self.path = self.getParam('vmware','path')
		self.host = self.getParam('vmware','host')
		self.user = self.getParam('vmware','user')
		self.passwd = self.getParam('vmware','passwd')
		
	def getParam(self, section, param):
		self.conf.read(self.file)
		param = self.conf.get(section,param)
		return param

	def getVmx(self, vm):
		vmx = self.getParam(vm, 'label')
		return vmx
    
    
	def getMachines(self):
		self.conf.read(self.file)
		vms = self.conf.get('vmware', 'machines').split(",")
		return vms