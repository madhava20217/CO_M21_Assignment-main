class RegisterFile:
	def __init__(self):
		self.reg = ["0"*16]*8

	def getVal(self, index):
		if(index < 7):
			return self.reg[index]
		else:
			return self.flag

	def setVal(self, index, val):
		self.reg[index] = val
	
	def dump(self):
		for r in self.reg:
			print(r,end = " ")
		print()
		