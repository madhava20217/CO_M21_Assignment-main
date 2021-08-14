from sys import stdin

#global variables:
global linenumber           #line number of currently executing statement
global variablearr          #list of variables
global otherarr             #list of instructions, elements are 1D arrays
global operandsdict         #dictionary of operands

operandslist = ['add', 'sub', 'mov', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and',
                'not', 'cmp', 'jmp', 'jlt', 'jgt', 'je', 'hlt']

global instructionDictA
instructionDictA = {'add': '00000', 'sub': '00001', 'mul': '00110', 'xor': '01010', 'or': '01011', 'and':'01100'}

global instructionDictD
instructionDictD = {'ld': '00100', 'st':'00101'}

global instructionDictE
instructionDictE = {'jmp':'01111','jlt':'10000','jgt':'10001','je':'10010'}

global instructionDictB
instructionDictB = {'mov':'00010','rs':'01000','ls':'01001'}

global instructionDictC
instructionDictC = {'mov':'00011','not':'01101','cmp':'01110'}

global regDict
regDict = {'R0':'000', 'R1': '001', 'R2':'010', 'R3':'011', 'R4':'100', 'R5':'101', 'R6':'110', 'FLAGS':'111'}

global var_dict
var_dict = dict()
global label_dict
label_dict = {}


# takes in s(string) and size(int) returns binary string of size size
def toBinary(s,size):
    ans = ""
    if(s.isnumeric()):
        s = int(s)
    else:
        return "Invalid syntax"
    while(s > 0):
        if(s % 2 == 0):
            ans = "0" + ans;
        else:
            ans = "1" + ans;
        s = s//2

    if(len(ans)==size):
        return ans;
    elif(len(ans) < size):
        while(len(ans) != size):
            ans = "0" + ans
        return ans
    else:
        ans = ans[len(ans) - size:]
        return ans
    


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
    res = isValidTypeA(x)
    if(res):
        binary = ''

        #accounting for the op-code
        if(x[0] in instructionDictA.keys()): binary+=instructionDictA.get(x[0])+"00"

        #checking operand types:
        op1 = x[1]      #defining first operand
        op2 = x[2]      #defining second operand
        op3 = x[3]      #defining third operand

        binary+= regDict.get(op1) + regDict.get(op2) + regDict.get(op3)


        if(len(binary) == 16): return binary
        else: raise SyntaxError("General Syntax Error at line ", linenumber)

    else: return None


def isValidTypeA(operationArr):
    '''takes in array argument and determines if it is a valid type A
    syntax
    
    Takes into account, the following exceptions:
    1. Typos in instruction name or register name.                                                  DONE
    2. Illegal use of FLAGS register                                                                DONE
    3. Wrong syntax used for instructions (~add instruction being used as a type B instruction)     DONE
    
    For the third part, mainly taking care of the nature of operands.'''

    if(len(operationArr) != 4):                                             #if length is not equal to 4, which is the length of typeA
        raise SyntaxError("General Syntax Error at line: ", linenumber)
        return False
    
    if(operationArr[0].strip() not in instructionDictA.keys()):                            #if instruction not in typeA list
        return False

    for i in range(1, 4):                                                   #checking operands
        tempReg = operationArr[i].strip()
        if(tempReg not in regDict.keys()):                          #if it is not in the list of registers, three cases ensue
            if(tempReg in var_dict.keys()):                                     #it is a variable
                raise Exception("Wrong syntax used for instructions at line: ", linenumber)
            if(tempReg in label_dict.keys()):
                raise Exception("Wrong syntax used for instructions at line: ", linenumber)
            if(tempReg[0] == '$'):
                raise Exception("Wrong syntax used for instructions at line: ", linenumber)
            else:
                raise Exception("Wrong syntax used for instructions at line: ", linenumber)
        if(tempReg == "FLAGS"):                                         #if it is the FLAGS register
                raise Exception("Illegal use of FLAGS register at line: ", linenumber)
            
    return True


#is valid variable instruction, returns boolean if the instructions is a valid var function 
#along with updating var_dict dictionary
def validVarInstruction(ins,location):
    global var_dict
    ins = ins.split()
    if(len(ins) != 2): return False
    if(ins[0] != 'var'): return False
    if(ins[1] in regDict.keys()): return False
    if(ins[1] in var_dict.keys()): return False #multiple declaration of single variable
    if(ins[1] in operandslist): return False
    ''' add more dict check here once they are declared above '''
    #check if it is alphanum or has underscores:
    for ch in ins[1]:
        if(ch.isalnum() or (ch == '_')): continue
        else: return False
    location = bin(location)[2:]
    var_dict[ins[1]] = "{:08d}".format(int(location))
    return True
def isValidVar(ins):
    global var_dict
    return (ins in var_dict.keys())

def isValidTypeD(ins):
    #takes in string and finds out if type matches or no
    x = ins.split()
    if len(x) != 3:
        return False
    return (x[0] in instructionDictD.keys())

def typeDInstruction(line):
    '''assumes ins is of type D,
    Takes in string argument and returns its corresponding binary string
    returns error if the registers or memory address are invalid

    types of error:
    use of undefined variable address
    misuse of labels as variables
    Illegal use of flag register '''
    ins = line.split()
    binary = instructionDictD[ins[0]]
    if (ins[1] == "FLAGS"):
        #error invalid register
        raise Exception("Illegal use of flag register at line: %d", linenumber)
    elif(isValidVar(ins[1]) == True):
        raise Exception("Wrong syntax used for the instruction at line: %d", linenumber)
    elif(ins[1] in label_dict.keys()):
        raise Exception("Wrong syntax used for the instruction at line: %d", linenumber)
    elif(isValidImmediate(ins[1]) == True):
        raise Exception("Wrong syntax used for the instruction at line: %d", linenumber)
    elif (ins[1] not in regDict.keys()):
        raise Exception("Typo in register name at line: %d", linenumber)
    else:
        binary = binary + regDict[ins[1]]

    if(ins[2] in label_dict.keys()):
        raise Exception("Misuse of labels as variables at line: %d", linenumber)
    elif(isValidVar(ins[2]) == False):
        raise Exception("Use of undefined Variable address at line: %d", linenumber)
    else:
        binary = binary + var_dict[ins[2]]

    return binary

def isValidTypeE(ins):
    #takes in string and ifnds out if type mathces or not
    x = ins.split()
    if len(x) != 2:
        return False
    return (x[0] in instructionDictE.keys());

def typeEInstruction(line):
    '''assumes ins is of type E,
    Takes in string argument and returns its corresponding binary string

    types of error:
    misuse of variables as labels
    use of undefined labels'''
    ins = line.split()
    binary = instructionDictE[ins[0]] + "000"

    if(isValidVar(ins[1]) == True):
        #error
        raise Exception("misuse of variables as labels at line: %d", linenumber)
    elif(validLabel(ins[1]) == False):
        raise Exception("use of undefined labels at line: %d", linenumber)
    else:
        binary = binary + label_dict[ins[1]]

    return binary

def typeFInstruction(ins):
    '''Takes in string argument and returns its corresponding binary.
    Optional: can also raise an error depending on the boolean value numberHalts

    Operands:
        1. String ins for the instruction
        2. boolean numberHalts which checks if the number of halts are not >1, default value is true
        
    Possible Errors:
    1. Wrong syntax used for instructions
    2. hlt not being used as the last instruction'''
    
    if(ins.strip() == 'hlt'):
        return "10011"+11*'0'
    else:
        raise Exception("Wrong syntax used for instruction at line: %d", linenumber)

def typeBInstruction(instruction):
    instruction = instruction.strip()
    word_list = instruction.split()
    if(len(word_list)!=3):
        raise Exception("General Syntax Error at line: {}".format(linenumber))
    binary_equivalent ="";
    # First word
    binary_equivalent += instructionDictB[word_list[0]] 
    # second word
    if word_list[1] in regDict and word_list[1] != "FLAGS":
        binary_equivalent += regDict[word_list[1]]
    elif word_list[1] == "FLAGS":
        raise Exception("Illegal use of flag register at line: {}".format(linenumber))
    elif word_list[1] in var_dict:
        raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
    elif word_list[1] in label_dict:
        raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
    elif isValidImmediate(word_list[1]):
        raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
    else:
        raise Exception("Typo in register name at line: {}".format(linenumber))
    #third word
    if word_list[2] == "FLAGS":
        raise Exception("Illegal use of flag register at line: {}".format(linenumber))
    elif word_list[2] in var_dict:
        raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
    elif word_list[2] in label_dict:
        raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
    elif word_list[2] in regDict:
        raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
    elif(word_list[2][0] != "$"):
        raise Exception("General Syntax Error at line: {}".format(linenumber))
    elif isValidImmediate(word_list[2]):
        word_list[2] = word_list[2][1:]
        temp = bin(int(word_list[2]))[2:]
        binary_equivalent += "{:08d}".format(int(temp))
    else:
        raise Exception("Illegal Immediate values (less than 0 or more than 255) {}".format(linenumber))
    return binary_equivalent
def typeCInstruction(instruction):
    instruction = instruction.strip()
    word_list = instruction.split()
    if len(word_list)!=3:
        raise Exception("General Syntax Error at line: {}".format(linenumber))
    binary_equivalent = "";
    # First word
    binary_equivalent += instructionDictC[word_list[0]]
    binary_equivalent += "00000" 
    #second word
    if word_list[1] in regDict and word_list[1] != "FLAGS":
        binary_equivalent += regDict[word_list[1]]
    elif word_list[1] == "FLAGS":
        raise Exception("Illegal use of flag register at line: {}".format(linenumber))
    elif word_list[1] in var_dict:
        raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
    elif word_list[1] in label_dict:
        raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
    elif isValidImmediate(word_list[1]):
        raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
    else:
        raise Exception("Typo in register name at line: {}".format(linenumber))
    #3rd word
    if(word_list[0] == "mov"):
        if word_list[2] in regDict:
            binary_equivalent += regDict[word_list[2]]
        elif word_list[2] in var_dict:
            raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
        elif word_list[2] in label_dict:
            raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
        elif isValidImmediate(word_list[2]):
            raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
        else:
            raise Exception("Typo in register name at line: {}".format(linenumber))
    else:
        if word_list[2] in regDict and word_list[2] != "FLAGS":
            binary_equivalent += regDict[word_list[2]]
        elif word_list[2] == "FLAGS":
            raise Exception("Illegal use of flag register at line: {}".format(linenumber))
        elif word_list[2] in var_dict:
            raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
        elif word_list[2] in label_dict:
            raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
        elif isValidImmediate(word_list[2]):
            raise Exception("Wrong syntax used for the instruction at line: {}".format(linenumber))
        else:
            raise Exception("Typo in register name at line: {}".format(linenumber))
    return binary_equivalent
def isValidImmediate(immediate):
    if immediate[0] == "$":
        immediate = immediate[1:]
        if immediate.isdigit() == True:
            if(int(immediate) <=255 and int(immediate)>=0):
                return True
            else:
                return False
        else:
            return False
    else:
        return False
def isValidTypeB(instruction):
    instruction = instruction.strip()
    word_list = instruction.split()
    if len(word_list)!=3:
        return False
    if word_list[0] in ["rs","ls"]:
        return True
    if (word_list[0] == "mov" and word_list[2][1:].isdigit() == True):
        return True
    else:
        return False
def isValidTypeC(instruction):
    instruction = instruction.strip()
    word_list = instruction.split()
    if len(word_list)!=3:
        return False
    if word_list[0] in ["not","cmp"]:
        return True
    elif (word_list[0] == "mov" and word_list[2].isdigit() != True):
        return True
    else:
        return False
def validLabel(label_name):
    if label_name in regDict: 
        return False
    #change name of var_dict
    elif label_name in var_dict: 
        return False
    elif label_name in operandslist:
        return False
    elif label_name in label_dict:
        return False
    else:
        for letter in label_name:
            if (not letter.isalnum() and letter != '_'):
                return False
        return True
def main():
    '''The main function for the CO assignment "Winter" 2021'''

    
    haltflag = False
    variableflag = False
    global linenumber
    memaddresscount = 0     #counts the memory address/instruction number

    line_no = []
    ctr = 1
    input_arr = []

    for line in stdin:
        
        if line == '':
            break
        else:
            line = line.strip()
            #checking for empty line
            if(line == ""):
                continue
            else:
                input_arr.append(line)
                line_no.append(ctr)
                ctr = ctr+1
            

    #working with variables:
    i = 0
    while(i < len(input_arr)):
        x = input_arr[i].split()
        if(x[0] != "var"): break
        i+=1;
    
    var_arr = input_arr[0:i] 
    input_arr = input_arr[i:]
    var_line_no = line_no[0:i]
    line_no = line_no[i:]

    var_loc = len(input_arr)
    for i in range(0 , len(var_arr)):
        check = validVarInstruction(var_arr[i],var_loc+i)
        if(check == False):
            raise Exception("Unsupported variable name format at line %d", var_line_no[i])
    #variables processed
    #Checking for labels and removing them from the instruction line if found
    for i in range(0,len(input_arr)):
        linenumber = line_no[i]
        instruction = input_arr[i].split();
        if(instruction[0][-1] == ":"):
            instruction[0] = instruction[0][:len(instruction[0]) - 1]
            if(validLabel(instruction[0])):
                temp = bin(i)[2:]
                label_dict[instruction[0]] = "{:08d}".format(int(temp))
                input_arr[i] = input_arr[i][len(instruction[0]) + 1:]
                input_arr[i] = input_arr[i].strip()
            else:
                raise Exception("General Syntax Error at line {}".format(linenumber))
    #Labels processed

    
    #generating list consisting of output commands and to take care of the exceptions that may occur
    #feeding functions input and collecting outputs:

    #inputs: input_arr, var

    memaddresscount = 0         #memory address initialised
    output_list = []            #list for storing the output binary, each element is a 16-bit binary number
    haltFlag = False

    #handling last element not halt exception
    if(input_arr[-1].strip() != 'hlt'):
        raise Exception("hlt not being used as the last instruction at line: %d", memaddresscount)

    while(memaddresscount<len(input_arr)):
        linenumber = line_no[memaddresscount]
        if(input_arr[memaddresscount].strip() == 'hlt'):
            if(haltFlag): raise Exception("hlt not being used as the last instruction at line: %d", linenumber)
            else: haltFlag = True

        #for other instructions
        #6 categories: instr is a temporary variable for easier processing
        instr = input_arr[memaddresscount]
        instr = instr.strip().split()
        
        if(instr[0] in instructionDictA.keys() and isValidTypeA(instr)):
            output_list.append(typeAInstruction(input_arr[memaddresscount]))
        
        elif(instr[0] in instructionDictB.keys() and isValidTypeB(input_arr[memaddresscount])):
            output_list.append(typeBInstruction(input_arr[memaddresscount]))

        elif(instr[0] in instructionDictC.keys() and isValidTypeC(input_arr[memaddresscount])):
            output_list.append(typeCInstruction(input_arr[memaddresscount]))
        
        elif(instr[0] in instructionDictD.keys() and isValidTypeD(input_arr[memaddresscount])):
            output_list.append(typeDInstruction(input_arr[memaddresscount]))
        
        elif(instr[0] in instructionDictE.keys() and isValidTypeE(input_arr[memaddresscount])):
            output_list.append(typeEInstruction(input_arr[memaddresscount]))

        elif(instr[0] == 'hlt' and not haltFlag):
            output_list.append(typeFInstruction(input_arr[memaddresscount]))
        
        else:
            raise Exception("Typos in instruction name or register name at memory location: %d", linenumber)



        memaddresscount+=1      #incrementing memaddresscount for the next iteration

    #printing out to STDOUT
    for i in output_list:
        print(i)
main()
