class ExecutionEngine:
	def __init__(self, memory, register):
		self.memory = memory
		self.register = register
	
	def execute(self,instr,pc,cycle=0):
		opcode = instr[0:5]
		halted = False
		#pc increment by 1
		pc = "{:08}".format(int(bin(int(pc,2)+1)[2:]))

		if(opcode == "00000"):
			#for add instruction
			self.add(instr)
		elif(opcode == "00001"):
			#for sub instruction
			self.sub(instr)
		elif(opcode == "00010"):
			self.mov_imm(instr)
		elif(opcode == "00011"):
			self.mov_reg(instr)
		elif(opcode == "00100"):
			self.ld(instr)
		elif(opcode == "00101"):
			self.st(instr)
		elif(opcode == "00110"):
			#
		elif(opcode == "00111"):
			self.divide(instr)
		elif(opcode == "01000"):
			self.rs(instr)
		elif(opcode == "01001"):
			self.ls(instr)
		elif(opcode == "01010"):
			#
		elif(opcode == "01011"):
			#
		elif(opcode == "01100"):
			#
		elif(opcode == "01101"):
			self.invert(instr)
		elif(opcode == "01110"):
			self.cmp(instr)
		elif(opcode == "01111"):
			if(self.jmp(instr)== True):
				pc = instr[8:16]
		elif(opcode == "10000"):
			if(self.jlt(instr)== True):
				pc = instr[8:16]
		elif(opcode == "10001"):
			if(self.jgt(instr)== True):
				pc = instr[8:16]
		elif(opcode == "10010"):
			if(self.je(instr)== True):
				pc = instr[8:16]
		elif(opcode == "10011"):
			#
		
		return [halted,pc]
	def ld(self, instr):
		#binary string to integer
		reg_addr = int(instr[5:8],2)
		mem_addr = int(instr[8:16],2)
		#setting register value
		self.register.setVal(reg_addr, self.memory.getData(mem_addr))

	def st(self, instr):
		#binary string to integer
		reg_addr = int(instr[5:8],2)
		mem_addr = int(instr[8:16],2)
		#setting memory value
		self.memory.setData(mem_addr, self.register.getVal(reg_addr))
	def jmp(self, instr):
		return True 
		
	def jlt(self, instr):
		flags = self.register.getVal(7) 
		#vlge
		if(flags[-3] == '1'): return True
		else: return False
	def jgt(self, instr):
		flags = self.register.getVal(7) 
		#vlge
		if(flags[-2] == '1'): return True
		else: return False
	def je(self, instr):
		flags = self.register.getVal(7) 
		#vlge
		if(flags[-1] == '1'): return True
		else: return False
	def mov_imm(instr):
		register1 = int(instr[5:8],2)
		imm = int(instr[8:],2)
		self.register.setVal(register1,"{:016d}".format(int(bin(imm)[2:])))
	def rs(instr):
		register1 = int(instr[5:8],2)
		imm = int(instr[8:],2)
		result = int(self.register.getVal(register1)) >> imm
		self.register.setVal(register1,"{:016d}".format(int(bin(result)[2:])))
	def ls(instr):
		register1 = int(instr[5:8],2)
		imm = int(instr[8:],2)
		result = int(self.register.getVal(register1)) << imm
		self.register.setVal(register1,"{:016d}".format(int(bin(result)[2:])))
	def mov_reg(instr):
		register1 = int(instr[5:8],2)
		register2 = int(instr[5:8],2)
		self.register.setVal(register1,self.register.getVal(register2))
	def divide(instr):
		register1 = int(instr[5:8],2)
		register2 = int(instr[5:8],2)
		quotient = int(self.register.getVal(register1)) // int(self.register.getVal(register2))
		self.register.setVal(register1,"{:016d}".format(int(bin(quotient)[2:])))
	def invert(instr):
		register1 = int(instr[5:8],2)
		register2 = int(instr[5:8],2)
		output = self.register.getVal(register2)
		for i in range(0,16):
			if(output[i] == "0"):
				output[i] = "1"
			elif (output[i] == "1"):
				output[i] = "0"
		self.register.setVal(register1,output)
	def cmp(instr):
		register1 = int(instr[5:8],2)
		register2 = int(instr[5:8],2)
		val1 = int(self.register.getVal(register1))
		val2 = int(self.register.getVal(register2))
		flag
		if val1 > val2:
			flag = "{:016d}".format(int(bin(2)[2:]))
		elif val1 < val2:
			flag = "{:016d}".format(int(bin(4)[2:]))
		elif val1 == val2:
			flag = "{:016d}".format(int(bin(8)[2:]))
		self.register.setVal(7,flag)


		
	def add(instr):
		'''Input: string operand
			Output: adds two registers and checks for overflow
		function for adding operands and storing result
		have to check for overflow (+ve only)'''
		outputreg = int(instr[5:8], 2)
		regop1 = int(instr[8:11], 2)
		regop2 = int(instr[11:14], 2)
		regval1 = self.register.getVal(regop1)		#searching RF for value for 1
		regval2 = self.register.getVal(regop2)		#searching RF for value for 2
		sum = regval1 + regval2						#sum
		overflow = False							#determines overflow
		if len("{:016d}".format(int(bin(sum)[2:]))) > 16: overflow = True
		if(overflow):
			self.register.setVal(7, '0'*12+'1'+'0'*3)
			#overflow set in register file
		sum = sum[-1::-1]	#inverting
		sum = sum[0:16]		#taking first 16 bits
		sum = sum[-1::-1]	#inverting back
		self.register.setVal(outputreg, sum)

	def sub(instr):
		'''Input: string operand
		Output: subtracts two registers and checks for underflow
		If underflowed, sets answer to 0 and sets overflow bit'''
		outputreg = int(instr[5:8], 2)
		regop1 = int(instr[8:11], 2)
		regop2 = int(instr[11:14], 2)
		regval1 = self.register.getVal(regop1)
		regval2 = self.register.getVal(regop2)
		difference = regval1 - regval2		#subtraction
		if(difference<0):
			difference = 0
			self.register.setVal(7, '0'*12+'1'+'0'*3)	#setting FLAGS register overflow bit
		#no OVERFLOW can occur since operands are whole number containing registers
		#only need to check for underflow
		self.register.setVal(outputreg, difference)



