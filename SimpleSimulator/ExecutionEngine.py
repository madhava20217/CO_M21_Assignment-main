class ExecutionEngine:
	def __init__(self, memory, register):
		self.memory = memory
		self.register = register
	
	def execute(self,instr,cycle=0):
		opcode = instr[0:5]
		if(opcode == "00000"):
			#
		elif(opcode == "00001"):
			#
		elif(opcode == "00010"):
			#
		elif(opcode == "00011"):
			#
		elif(opcode == "00100"):
			load(self, instr)
		elif(opcode == "00101"):
			store(self, instr)
		elif(opcode == "00110"):
			#
		elif(opcode == "00111"):
			#
		elif(opcode == "01000"):
			#
		elif(opcode == "01001"):
			#
		elif(opcode == "01010"):
			#
		elif(opcode == "01011"):
			#
		elif(opcode == "01100"):
			#
		elif(opcode == "01101"):
			#
		elif(opcode == "01110"):
			#
		elif(opcode == "01111"):
			#
		elif(opcode == "10000"):
			#
		elif(opcode == "10001"):
			#
		elif(opcode == "10010"):
			#
		elif(opcode == "10011"):
			#
		
		return [halted,pc]
	
	def load(self, instr):
		#
	
	def store(self, instr):
		#