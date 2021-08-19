class Memory:
	def __init__(self):
		self.mem = ["0"*16]*256
		#input?

	def getData(self,index):
		#takes in index, returns the 
		return self.mem[index]
	
	def setData(self, index, val):
		self.mem[index] = val

	def dump(self):
		for m in self.mem:
			print(m)

	

