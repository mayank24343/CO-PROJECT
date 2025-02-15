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
    pass

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
        lines = f.readlines()
        binarycode = []
        for i in lines():
            try:
                decode(i)
                binarycode.append(i)
            except:
                binarycode.append("error encountered\n")

    #to write the generated binary to output file
    with open(output_file,'w') as f:
        f.writelines(binarycode)

            