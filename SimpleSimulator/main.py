from Memory import Memory
from ProgramCounter import ProgramCounter
from RegisterFile import RegisterFile
from ExecutionEngine import ExecutionEngine

def main():
	memory = Memory()
	registerFile = RegisterFile()
	executionEngine = ExecutionEngine(memory,registerFile)
	PC = ProgramCounter("0"*8)
	halted = False 
	cycle = 0

	while not halted:
		inst = memory.fetch(PC.getVal(),cycle)
		halted, nextPC = executionEngine.execute(inst,PC.getVal(),cycle)
		PC.dump()
		registerFile.dump()
		PC.update(nextPC)
		cycle += 1
	
	if __name__ == '__main__':
		main()