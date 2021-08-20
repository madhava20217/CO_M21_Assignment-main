import matplotlib.pyplot as plt
class Memory:
	def __init__(self):
		self.mem = ["0"*16]*256
		self.x = []
		self.y = []
		#input?

	def getData(self,index,cycle):
		#takes in index, returns the 
		self.x.append(cycle)
		self.y.append(index)
		return self.mem[index]
	
	def setData(self, index, val,cycle):
		self.x.append(cycle)
		self.y.append(index)
		self.mem[index] = val
	def dump(self):
		for m in self.mem:
			print(m)
	
	def scatterPlot(self):
		plt.scatter(self.x,self.y)
		plt.title('Memory address access scatter plot')
		plt.xlabel('Cycle')
		plt.ylabel('Memory Address')
		plt.show()
	


