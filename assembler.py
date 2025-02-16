labels = {}
curr = 0

def binary(num):
    b = ''
    if num == 0:
        return '0'
    while num>0:
        b+=str(num%2)
        num = num//2

    b = b[::-1]
    return b

def sext(num,n):
    if len(num) > n:
        return "error"
    else:
        while len(num) < n:
            num = num[0]+num

        return num

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

def register(reg):
    d = {'zero':'00000',
    'ra':'00001',
    'sp':'00010',
    'gp':'00011',
    'tp':'00100',
    't0':'00101',
    't1':'00110',
    't2':'00111',
    's0':'01000',
    'fp':'01000',
    's1':'01001',
    'a0':'01010',
    'a1':'01011',
    'a2':'01100',
    'a3':'01101',
    'a4':'01110',
    'a5':'01111',
    'a6':'10000',
    'a7':'10001',
    's2':'10010',
    's3':'10011',
    's4':'10100',
    's5':'10101',
    's6':'10110',
    's7':'10111',
    's8':'11000',
    's9':'11001',
    's10':'11010',
    's11':'11011',
    't3':'11100',
    't4':'11101',
    't5':'11110',
    't6':'11111'}

    if reg in d:
        return d[reg]
    else:
        try:
            reg = reg.split('x')
            b = binary(int(reg[1]))
            return sext(b,5)
        except:
            return 'invalid register'

def r_type(input):
    #to convert r type instruction to binary
    pass

def s_type(input):
    #to convert s type instruction to binary
    pass

def i_type(input):
    #to convert i type instruction to binary
    pass

def b_type(input):
    #to convert n type instruction to binary
    pass

def j_type(input):
    #to convert j type instruction to binary
    input = input.split()
    if input[0] == 'jal':
        opcode = "1101111"
        input = input[1].split(',')
        rd = register(input[0])
        dest = input[1]
        if dest in labels:
            imm = twoscomplement(labels[dest]-curr,20)
        else:
            imm = twoscomplement(int(dest),20)
        
        return imm[-20]+imm[-11:-1]+imm[-12]+imm[-19:-11]+rd+opcode

def bonus(input):
    #to convert reset and halt instruction to binary
    pass

def decode(input):
    #to decode aseembly instructions into 32 bit binary
    binary=""
    try:
        binary = r_type(input)
    except:
        try:
            binary = s_type(input)
        except:
            try:
                binary = i_type(input)
            except:
                try:
                    binary = s_type(input)
                except:
                    try:
                        binary = b_type(input)
                    except:
                        try:
                            binary = j_type(input)
                        except:
                            try:
                                binary = bonus(input)
                            except:
                                binary = "error : instruction does not match syntax for any instruction type\n"
    
    return binary

def assembler(input_file, output_file):
    
    #to read input file (assembly level instructions) and convert to 32 bit binary code
    with open(input_file,'r') as f:
        data = f.readlines()
        addr = 0
        lines = []
        for i in data:
            lines.append((addr,i))
            addr+=4

        binarycode = ["shit\n"]
        for i in lines:
            curr = i[0]
            try:
                k = i[1].split(':')
                if len(k)>1:
                    labels[k[0]] = i[0]
                    j = decode(k[1].strip(' '))
                else:
                    j = decode(k[0].strip(' '))
                binarycode.append(j)
            except:
                binarycode.append("error encountered\n")

    print(binarycode)
    #to write the generated binary to output file
    with open(output_file,'w') as f:
        f.writelines(binarycode)

#assembler('a.txt','b.txt')