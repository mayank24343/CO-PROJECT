import sys

#useful functions 
def binary(num):
    b = ''
    if num == 0:
        return '0'
    while num>0:
        b+=str(num%2)
        num = num//2

    b = b[::-1]
    return '0'+b

def sext(num,n):
    while len(num) < n:
        num = num[0]+num
    while len(num) > n:
        num = num[1:]

    return num
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

def binary_to_decimal(num):
    flag = False
    if num[0] == '1':
        newnum = ''
        for i in num:
            if i=='0':
                newnum+='1'
            else:
                newnum+='0'
        flag = True
        num = newnum

    num = num[::-1]
    dec = 0
    for i in range(len(num)):
            dec+= (2**i)*int(num[i])
    
    if flag:
        return -(dec+1)
    else:
        return dec

def decimal_to_hex(num):
    hex = ''
    d = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'A',11:'B',12:'C',13:'D',14:'E',15:'F'}
    while num>0:
        hex+= d[num%16]
        num//= 16

    hex = hex[::-1]
    return hex

def binary_to_hex(b):
    hex = ''
    d = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'A',11:'B',12:'C',13:'D',14:'E',15:'F'}
    groups = [b[i:i+4] for i in range(0,len(b),4)]
    for i in groups:
        hex+= d[binary_to_decimal('0'+i)]
    return hex

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
    global registers
    global data_memory
    global PC 

    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    rd = instruction[20:25]
    imm = instruction[0:12]

    if funct3 == '010':
        registers[rd] = data_memory.setdefault('0x'+binary_to_hex(twoscomplement(registers[rs1]+binary_to_decimal(imm),32)),0)
        pass

    return 4 

def addi(instruction):
    global registers
    global data_memory
    global PC 

    rs = instruction[12:17]
    funct3 = instruction[17:20]
    rd = instruction[20:25]
    imm = instruction[0:12]

    if funct3 == '000':
        registers[rd] = registers[rs]+binary_to_decimal(imm)

    return 4

def jalr(instruction):
    global registers
    global data_memory
    global PC 

    rs = instruction[12:17]
    funct3 = instruction[17:20]
    rd = instruction[20:25]
    imm = instruction[0:12]

    if funct3 == '000':
        final_address = (registers[rs] + binary_to_decimal(imm))
        registers[rd] = PC + 4
        
        return final_address-PC

#s type 
def s_type(instruction):
    global data_memory
    global PC

    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    imm4_0 = instruction[20:25]
    imm11_5 = instruction[0:7]

    num = imm11_5+imm4_0
    data_memory['0x'+binary_to_hex(twoscomplement(registers[rs1]+binary_to_decimal(num),32))] = registers[rs2]
    return 4

# b type 
def b_type(instruction):
    global registers
    global data_memory
    global PC 

    rs2 = instruction[7:12]
    rs1 = instruction[12:17]
    funct3 = instruction[17:20]
    
    imm = instruction[0] + instruction[24] + instruction[1:7] + instruction[20:24] + '0'
    imm = binary_to_decimal(imm)  

    if funct3 == '000':  # beq
        if registers[rs1] == registers[rs2] and imm != 0:
            return imm
        elif registers[rs1] == registers[rs2] and imm == 0 and rs1==rs2 and rs2 == '00000':
            return "halt"
        else:
            return 4
    elif funct3 == '001':  # bne
        if registers[rs1] != registers[rs2]:
            return imm
        else:
            return 4
    else:
        return 4

#j type 
def j_type(instruction):
    global registers
    global PC

    rd = instruction[20:25]
    
    imm = instruction[0] + instruction[12:20] + instruction[11] + instruction[1:11] + '0'
    imm = binary_to_decimal(sext(imm, 21))

    registers[rd] = PC + 4

    return imm

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
