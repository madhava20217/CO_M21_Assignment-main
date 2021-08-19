class RegisterFile:
	def __init__(self):
		self.reg = ["0"*16]*8

	def getVal(self, index):
			return self.reg[index]

	def setVal(self, index, val):
		self.reg[index] = val
	
	def dump(self):
		for r in self.reg:
			print(r,end = " ")
		print()
		