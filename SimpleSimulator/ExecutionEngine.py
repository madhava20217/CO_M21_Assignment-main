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
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			self.mov_imm(instr)
		elif(opcode == "00011"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			self.mov_reg(instr)
		elif(opcode == "00100"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			self.ld(instr)
		elif(opcode == "00101"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			self.st(instr)
		elif(opcode == "00110"):
			#for mul instruction
			self.mul(instr)
		elif(opcode == "00111"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			self.divide(instr)
		elif(opcode == "01000"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			self.rs(instr)
		elif(opcode == "01001"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			self.ls(instr)
		elif(opcode == "01010"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			#for xor operation
			self.logicalxor(instr)
		elif(opcode == "01011"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			#for OR instruction
			self.logicalor(instr)
		elif(opcode == "01100"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			#for AND instruction
			self.logicaland(instr)
		elif(opcode == "01101"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			self.invert(instr)
		elif(opcode == "01110"):
			self.cmp(instr)
		elif(opcode == "01111"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			if(self.jmp(instr)== True):
				pc = instr[8:16]
		elif(opcode == "10000"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			if(self.jlt(instr)== True):
				pc = instr[8:16]
		elif(opcode == "10001"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			if(self.jgt(instr)== True):
				pc = instr[8:16]
		elif(opcode == "10010"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			if(self.je(instr)== True):
				pc = instr[8:16]
		elif(opcode == "10011"):
			self.register.setVal(7, '0'*16)					#resetting FLAGS
			halted = True
		
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
	def mov_imm(self, instr):
		register1 = int(instr[5:8],2)
		imm = int(instr[8:],2)
		self.register.setVal(register1,"{:016d}".format(int(bin(imm)[2:])))
	def rs(self, instr):
		register1 = int(instr[5:8],2)
		imm = int(instr[8:],2)
		result = int(self.register.getVal(register1),2) >> imm
		self.register.setVal(register1,"{:016d}".format(int(bin(result)[2:])))
	def ls(self, instr):
		register1 = int(instr[5:8],2)
		imm = int(instr[8:],2)
		result = int(self.register.getVal(register1),2) << imm
		self.register.setVal(register1,"{:016d}".format(int(bin(result)[2:])))
	def mov_reg(self, instr):
		register1 = int(instr[5:8],2)
		register2 = int(instr[5:8],2)
		self.register.setVal(register1,self.register.getVal(register2))
	def divide(self, instr):
		register1 = int(instr[5:8],2)
		register2 = int(instr[5:8],2)
		quotient = int(self.register.getVal(register1),2) // int(self.register.getVal(register2),2)
		self.register.setVal(register1,"{:016d}".format(int(bin(quotient)[2:])))
	def invert(self, instr):
		register1 = int(instr[5:8],2)
		register2 = int(instr[5:8],2)
		output = self.register.getVal(register2)
		inverted_output = ""
		for i in range(0,16):
			if(output[i] == "0"):
				inverted_output+= "1"
			elif (output[i] == "1"):
				inverted_output += "0"
		self.register.setVal(register1,output)
	def cmp(self, instr):
		register1 = int(instr[5:8],2)
		register2 = int(instr[5:8],2)
		val1 = int(self.register.getVal(register1),2)
		val2 = int(self.register.getVal(register2),2)
		if val1 > val2:
			flag = "{:016d}".format(int(bin(2)[2:]))
		elif val1 < val2:
			flag = "{:016d}".format(int(bin(4)[2:]))
		elif val1 == val2:
			flag = "{:016d}".format(int(bin(8)[2:]))
		self.register.setVal(7,flag)


		
	def add(self, instr):
		'''Input: string operand
			Output: adds two registers and checks for overflow
		function for adding operands and storing result
		have to check for overflow (+ve only)'''
		outputreg = int(instr[5:8], 2)
		regop1 = int(instr[8:11], 2)
		regop2 = int(instr[11:14], 2)
		regval1 = int(self.register.getVal(regop1),2)
		regval2 = int(self.register.getVal(regop2),2)
		sum = regval1 + regval2						#sum
		sum = "{:016d}".format(int(bin(sum)[2:]))
		if len(sum)>16:
			self.register.setVal(7, '0'*12+'1'+'0'*3)
			#overflow set in register file
		else:
			self.register.setVal(7, '0'*16)			#in case no overflow, resetting FLAGS
		sum = sum[-1:-17:-1]	#inverting and taking last 16 bits
		sum = sum[-1::-1]	#inverting back
		self.register.setVal(outputreg, sum)

	def sub(self, instr):
		'''Input: string operand
		Output: subtracts two registers and checks for underflow
		If underflowed, sets answer to 0 and sets overflow bit'''
		outputreg = int(instr[5:8], 2)
		regop1 = int(instr[8:11], 2)
		regop2 = int(instr[11:14], 2)
		regval1 = int(self.register.getVal(regop1),2)
		regval2 = int(self.register.getVal(regop2),2)
		difference = regval1 - regval2		#subtraction
		if(difference<0):
			difference = 0
			self.register.setVal(7, '0'*12+'1'+'0'*3)	#setting FLAGS register overflow bit
		else:
			self.register.setVal(7, '0'*16)				#in case no underflow, resetting FLAGS
		
		#no OVERFLOW can occur since operands are whole number containing registers
		#only need to check for underflow
		
		difference = "{:016d}".format(int(bin(difference)[2:]))	#converting to bin
		self.register.setVal(outputreg, difference)


	def mul(self, instr):
		'''Input: string operand
		Output: multiplies the two numbers in the registers,
		sets the overflow bit if needed'''
		outputreg = int(instr[5:8], 2)
		regop1 = int(instr[8:11], 2)
		regop2 = int(instr[11:14], 2)
		regval1 = int(self.register.getVal(regop1),2)
		regval2 = int(self.register.getVal(regop2),2)
		product = regval1 * regval2
		if product >= 2**16:
			self.register.setVal(7, '0'*12+'1'+'0'*3)		#sets flag register
			product = product%65535							#taking modulus
		else:
			self.register.setVal(7, '0'*16)					#in case no overflow, resetting FLAGS
		product = "{:016d}".format(int(bin(product)[2:]))
		#product = product[-1:-17:-1]	#inverting and taking last 16 bits
		#product = product[-1::-1]	#inverting back
		self.register.setVal(outputreg, product)

	def logicalxor(self, instr):
		'''Input: string operand
		output: takes xor of the two numbers in the registers, sets overflow bits if needed'''
		outputreg = int(instr[5:8], 2)
		regop1 = int(instr[8:11], 2)
		regop2 = int(instr[11:14], 2)
		regval1 = int(self.register.getVal(regop1),2)
		regval2 = int(self.register.getVal(regop2),2)
		xorval = regval1^regval2
		xorval = "{:016d}".format(int(bin(xorval)[2:]))
		if(len(xorval>16)):self.register.setVal(7, '0'*12+'1'+'0'*3)
		xorval = xorval[-1:-17:-1]	#taking first 16 bits
		xorval = xorval[-1::-1]	
		self.register.setVal(outputreg, xorval)
		self.register.setVal(7, '0'*16)	#resetting FLAGS

	def logicalor(self, instr):
		'''Input: takes string operand
		Output: writes back to register file, sets overflow bit if required (doesn't)'''
		outputreg = int(instr[5:8], 2)
		regop1 = int(instr[8:11], 2)
		regop2 = int(instr[11:14], 2)
		regval1 = int(self.register.getVal(regop1),2)
		regval2 = int(self.register.getVal(regop2),2)
		orval = regval1|regval2
		orval = "{:016d}".format(int(bin(orval)[2:]))
		#since OR can't set overflow bits, no overflow checks implemented
		self.register.setVal(outputreg, orval)
		self.register.setVal(7, '0'*16)	#resetting FLAGS

	def logicaland(self, instr):
		'''Input: takes string operand
		Output: writes back to register file after computing AND of the two registers
		Does not set overflow bits, since it can't overflow with bitwise operations'''
		outputreg = int(instr[5:8], 2)
		regop1 = int(instr[8:11], 2)
		regop2 = int(instr[11:14], 2)
		regval1 = int(self.register.getVal(regop1),2)
		regval2 = int(self.register.getVal(regop2),2)
		andval = regval1&regval2
		andval = "{:016d}".format(int(bin(andval)[2:]))
		self.register.setVal(outputreg, andval)
		self.register.setVal(7, '0'*16)	#resetting FLAGS
