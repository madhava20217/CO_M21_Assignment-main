global instructionDictA
instructionDictA = {'add': '00000', 'sub': '00001', 'mul': '00110', 'xor': '01010', 'or': '01011', 'and':'01100'}

                        
global regDict
regDict = {'R0':'000', 'R1': '001', 'R2':'010', 'R3':'011', 'R4':'100', 'R5':'101', 'R6':'110', 'FLAGS':'111'}







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
def type_b_instruction(instruction):
    instruction = instruction.strip()
    word_list = instruction.split(" ")
    if(len(word_list)!=3):
        raise SyntaxError("General Syntax Error")
    binary_equivalent ="";
    # First word
    if word_list[0] == "mov" :
        binary_equivalent += "00010"
    elif word_list[0] == "rs":
        binary_equivalent += "01000"
    elif word_list[0] == "ls":
        binary_equivalent += "01001"
    else:
        raise SyntaxError("??")
    # second word
    if word_list[1] in regDict:
        binary_equivalent += regDict[word_list[1]]
    else:
        raise SyntaxError("Typos in instruction name or register name")
    #third word
    if(world_list[2][0] != "")
    if valid_immediate(word_list[2]) == True:
        temp = bin(int(word_list[2]))[2:]
        binary_equivalent += "{:08d}".format(int(temp))
        print(binary_equivalent);
    else:
        raise SyntaxError("Illegal Immediate values (less than 0 or more than 255)")
def type_c_instruction(instruction):
    instruction = instruction.strip()
    word_list = instruction.split(" ")
    if len(word_list)!=3:
        raise SyntaxError("General Syntax Error")
    binary_equivalent = "";
    # First word
    if word_list[0] == "mov" :
        binary_equivalent += "00011"
    elif word_list[0] == "not":
        binary_equivalent += "01101"
    elif word_list[0] == "cmp":
        binary_equivalent += "01110"
    else:
        raise SyntaxError("??")
    binary_equivalent += "00000"
    if word_list[1] in regDict:
        binary_equivalent += regDict[word_list[1]]
    else:
        raise SyntaxError("Typos in instruction name or register name")
    if word_list[2] in regDict:
        binary_equivalent += regDict[word_list[2]]
    else:
        raise SyntaxError("Typos in instruction name or register name")
    return binary_equivalent
def valid_immediate(immediate):
    if immediate.isdigit() == True:
        if(int(immediate) <=255 and int(immediate)>=0):
            return True
        else:
            return False
    else:
        return False
def valid_label(label,label_dict):
    if label in label_dict:
        return True
    else:
        return False
    



        

