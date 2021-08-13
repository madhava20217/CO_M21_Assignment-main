from sys import stdin

#global variables:
global variablearr          #list of variables
global otherarr             #list of instructions, elements are 1D arrays
global labelarr             #list of labels, elements are 1D arrays
global operandsdict         #dictionary of operands
global 

variablearr = []    #stores variables declared, which are memory locations, elements are strings
otherarr = []       #stores stuff besides variables, elements are 1D array elements
labelarr = []       #stores labels: elements are 1D array comprising of label name and memory address
operandslist = ['add', 'sub', 'mov', 'ld', 'st', 'mul', 'div', 'rs', 'ls', 'xor', 'or', 'and',
                'not', 'cmp', 'jmp', 'jlt', 'jgt', 'je', 'hlt']

def main():
    '''The main function for the CO assignment "Winter" 2021'''

    
    haltflag = False
    variableflag = False

    linecount = 0           #counts the line number
    memaddresscount = 0     #counts the memory address/instruction number

    for line in stdin:
        
        linecount+=1
        
        if line == '':
            break
        else:
            line.strip().split()
            
            #taking care of variables list: initialising variablearr list.
            if line[0] == 'var':
                
                #taking care of exception, encountering var declaration in the middle of the array
                if(variableflag):
                    raise Exception("Variables not declared at the beginning before usage at line: %d", linecount)
                
                #raising exception if number of elements in 'line' are not equal to 2.
                if(len(line) != 2):
                    raise Exception("Invalid syntax at line: %d", linecount)

                #appending to list of variables, if no error encountered at this point.
                if(!isvalidvariablename(line[1])):
                    raise Exception("Unsupported variable name format at line %d", linecount)
                variablearr.append(line[1])

            
            #taking care of other types: instructions, labels, other exceptions

            if(line[0] != 'var'):
                variableflag = True     #setting variableflag to True after encountering first

                #labels:
                if(line[0] not in operandslist):
                    if(line[0][-1] == ":" and isvalidvariablename(line[0], 'label')):
                        #label found, adjust accordingly
                    else:
                        raise Exception("Invalid syntax at line: %d", linecount)


                otherarr.append(line);







#helper which may be filled later

def isvalidvariablename(string, type = 'var'):
    '''checks if the variable name given is satisfactory and in accordance with the ISA
    Can also be used for a label if accounted for the last colon in place, when passing the argument'''
    
    #taking label parameter, adjusting accordingly
    if(type == 'label'):
        string = string[0:-1]
    
    string.split("_")
    toReturn = True
    for x in string:
        toReturn = (toReturn and x.isalnum())
    return toReturn