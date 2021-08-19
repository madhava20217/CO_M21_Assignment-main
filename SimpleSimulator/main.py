from Memory import Memory
from ProgramCounter import ProgramCounter
from RegisterFile import RegisterFile
from ExecutionEngine import ExecutionEngine
from sys import stdin

def main():
	memory = Memory()
	registerFile = RegisterFile()
	executionEngine = ExecutionEngine(memory,registerFile)
	PC = ProgramCounter("0"*8)
	halted = False 
	cycle = 0
	
	ctr = 0
	for line in stdin:
		if(line == ''):
			break
		else:
			memory.setData(ctr, line)
			ctr+=1

	while not halted:
		inst = memory.fetch(PC.getVal(),cycle)
		halted, nextPC = executionEngine.execute(inst,PC.getVal(),cycle)
		PC.dump()
		registerFile.dump()
		PC.update(nextPC)
		cycle += 1
	
if __name__ == '__main__':
	main()