import sys

#useful functions 
#write the functions i've used here according to whatt i explained each function does, some are similar to that of assembler
def twoscomplement(num,len):
    if num >= 0:
        tc = binary(num)
    else:
        b = binary(-num)
        tc = ''
        flag = 0
        for i in b[::-1]:
            if flag:
                if i == "0":
                    tc+="1"
                else:
                    tc+="0"
            else:
                tc += i
            if i == "1":
                flag = 1
        tc = tc[::-1]
        tc = "1"+tc
    tc = sext(tc,len)
    return tc 

#initialising pc counter to zero
PC = 0

#initialising registers x0,x1..x31 to zero
registers = {}
for i in range(32):
    registers[sext(binary(i),5)] = 0

registers['00010'] = 380

#initialising memory 0x00010000 .. 0x0001007C to zero
data_memory = {}
for i in range(1000,1008):
    for j in ['0','4','8','C']:
        data_memory['0x000'+str(i)+j] = 0

#dictionary with opcodes
opcode = {
'0110011':'r',#rtype 
'0000011':'lw', #lw
'0010011':'addi', #addi
'1100111':'jalr', #jalr
'0100011':'sw', #sw
'1100011':'b', #b type 
'1101111':'j' #j type 
}

#rtype 
def r_type(instruction):
    global registers
    global PC

    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    rd = instruction[20:25]
    funct7 = instruction[0:7]
    if funct3 == '000':
        if funct7 == '0000000':
            registers[rd] = registers[rs1] + registers[rs2]  #add
        elif funct7 == '0100000':
            registers[rd] = registers[rs1] - registers[rs2]  #sub
    elif funct3 == '010':
        if registers[rs1] < registers[rs2]:  
            registers[rd] = 1  #slt
        else:
            registers[rd] = 0
    elif funct3 == '101':
        registers[rd] = registers[rs1] >> binary_to_decimal(sext(binary(registers[rs2]), 5))  #srl
    elif funct3 == '110':
        registers[rd] = registers[rs1] | registers[rs2]  #or
    elif funct3 == '111':
        registers[rd] = registers[rs1] & registers[rs2] #and

    return 4

#i type
def lw(instruction):
    pass

def addi(instruction):
    pass

def jalr(instruction):
    pass

#s type 
def s_type(instruction):
    pass

# b type 
def b_type(instruction):
    pass

#j type 
def j_type(instruction):
    pass

def simulator(input_file,output_file):
    global PC

    #reading from file and creating instruction memory
    with open(input_file,'r') as f:
        instruction_memory = f.readlines()
        instruction_memory = [i.strip('\n') for i in instruction_memory]


    with open(output_file,'w') as f:
        #executing instructions 
        while PC != len(instruction_memory)*4:
            #print()
            #print(PC//4)
            instruction = instruction_memory[PC//4]
            op = instruction[-7:]
            #print(opcode[op])
            op = opcode[op]
            if op == 'r':
                PC += r_type(instruction)
            elif op == 'lw':
                PC += lw(instruction)
            elif op == 'addi':
                PC += addi(instruction)
            elif op == 'jalr':
                PC += jalr(instruction)
            elif op == 'sw':
                PC += s_type(instruction)
            elif op == 'b':
                result = b_type(instruction)
                if result == "halt":
                    output = ""
                    output2 = ""
                    for i in range(32):
                        output += str(registers[sext(binary(i),5)])+" "
                        output2 += '0b'+twoscomplement(registers[sext(binary(i),5)],32)+" "
                    #f.write(f"{PC} "+output+"\n")
                    f.write(f"0b{sext(binary(PC),32)} "+output2+"\n")
                    break
                else:
                    PC += result
            elif op == 'j':
                PC += j_type(instruction)

            registers['00000'] = 0

            output = ""
            output2 = ""
            for i in range(32):
                output += str(registers[sext(binary(i),5)])+" "
                output2 += '0b'+twoscomplement(registers[sext(binary(i),5)],32)+" "
            f.write(f"0b{sext(binary(PC),32)} "+output2+"\n")


        l = list(data_memory.keys())
        l = l[0]
        for i in range(1000,1008):
            for j in ['0','4','8','C']:
                f.write(f"{'0x000'+str(i)+j}:0b{twoscomplement(data_memory['0x000'+str(i)+j],32)}\n")
            
simulator(sys.argv[1],sys.argv[2])
