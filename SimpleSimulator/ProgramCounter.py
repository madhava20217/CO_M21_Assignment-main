#string return types
class ProgramCounter:
	def __init__(self, val):
		self.pc = val
	
	def getVal(self):
		#converty to binary before returning
		return self.pc
	
	def update(self, val):
		#val is integer (ig)
		self.pc = val
	
	def dump(self):
		#to do