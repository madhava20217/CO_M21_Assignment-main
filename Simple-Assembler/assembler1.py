global instructionDictA
instructionDictA = {'add': '00000', 'sub': '00001', 'mul': '00110', 'xor': '01010', 'or': '01011', 'and':'01100'}

                        
global regDict
regDict = {'R0':'000', 'R1': '001', 'R2':'010', 'R3':'011', 'R4':'100', 'R5':'101', 'R6':'110', 'FLAGS':'111'}

global var 
var = dict()








def typeAInstruction(x):
    '''Takes in input for type A instruction, tests if it is valid 
    and returns the corresponding binary code for the instruction
    Requires: string input
    Functions used:
        1. isValidTypeA: checks if string is a valid expression 
        of type A
        2. isValidImm: checks if immediate is a valid immediate
        3. isValidReg: checks if register is valid.
    '''
    x = x.split()
    if(isValidTypeA(x)):
        binary = ''
        
        #accounting for the op-code
        if(x[0] in instructionDictA.keys()): binary+=instructionDictA(x[0]);

        if(isValidReg(x[1]) and isValidReg(x[2]) and isValidReg(x[3])):
            binary+= regDict(x[1]) + regDict(x[2]) + regDict(x[3])

        if(len(binary) == 16): return binary
        else: raise SyntaxError("Typos in instruction or register name")


        
        
    else: raise SyntaxError("General Syntax Error")



def isValidType(operationArr):
    '''takes in array argument and determines if it is a valid type A 
    syntax'''

    if(len(operationArr) != 4): return False
    if(operationArr[0] not in instructionDictA): return False
    for i in range(1, 4):
        if(!isValidReg(operationArr[1])): return False
    return True


def isValidReg(reg):
    '''except flag'''
    regDictA = {'R0':'000', 'R1': '001', 'R2':'010', 'R3':'011', 'R4':'100', 'R5':'101', 'R6':'110'}
    return (reg in regDictA.keys())



#is valid variable instruction, returns boolean if the instructions is a valid var function 
def validVarInstruction(ins):
    ins = ins.split()
    if(len(ins) != 2) return false
    if(ins[0] != 'var') return false 
    if(ins[1] in regDict.keys()) return false
    if(ins[1] in instructionDictA.keys()) return false 
    ''' add more dict check here once they are declared above '''
    #check if it is alphanum or has underscores:
    for ch in ins[1]:
        if(ch.isalnum() or (ch == '_')) continue
        else return false
    global var
    ''' add mechanism to give value to var as well (depending on program size) '''
    var[ins[1]] = 1
    return true