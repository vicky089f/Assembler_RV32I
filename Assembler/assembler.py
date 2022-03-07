import pandas as pd
import re
import inst
import register as reg
import os
import fnmatch

f = open("code1.txt")
lines = f.readlines()
asm = [line.strip() for line in lines]
f.close()
print(asm)

label = []
for i in range(len(asm)):
    if(re.search('\:',asm[i])):
        label.append([re.split(":",asm[i])[0], 4*i])
        asm[i] = re.split(":",asm[i])[1]
        asm[i] = asm[i].strip()

# print(asm)
# print(label)
asm1 = []
for i in range(len(asm)):
    asm1.append(re.split(" ", asm[i], 1))

# print(asm1)
asmdf = pd.DataFrame(asm1)

print(asmdf)

op = []
f3 = []
f7 = []
for x in asmdf[0]:
    i = inst.instDf.index[inst.instDf['name'] == x].tolist()
    op.append(inst.instDf['opcode'][i[0]])
    f3.append(inst.instDf['funct3'][i[0]])
    f7.append(inst.instDf['funct7'][i[0]])
# print(op,f3,f7)

asm2 = []
for x in asmdf[1]:
    asm2.append(re.split( (",|\(|\)|:") ,x))

for x in asm2:
    if (len(x)>3):
        x.pop()

print(asm2)

inst_code = []
for i in range(len(op)):
    if(op[i] == "0110111" or op[i] == "0010111"):
        # ******************************LUI******************************
        rd = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][0]].tolist()[0]]
        if(int(asm2[i][1]) >= 0):
            imm = '{:020b}'.format(int(asm2[i][1]))
        else:
            imm = '{:020b}'.format(2**12 + int(asm2[i][1]))
        inst_code.append('{:08x}'.format(int(imm + rd + op[i], base=2)))

    elif(op[i] == "1101111"):
        # ******************************JAL******************************
        rd = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][0]].tolist()[0]]
        for x in label:
            if x[0] == asm2[i][1]:
                if x[1] >= 4*i:
                    imm = '{:020b}'.format(int((x[1] - 4*i)/2))
                else:
                    imm = '{:020b}'.format(2**12 + int((x[1] - 4*i)/2))
        inst_code.append('{:08x}'.format(int(imm[0] + imm[-10:] + imm[10] + imm[1:9] + rd + op[i], base=2)))


    elif(op[i] == "1100111"):
        # ******************************JALR******************************
        rd = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][0]].tolist()[0]]
        rs1 = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][1]].tolist()[0]]
        if(int(asm2[i][2]) >= 0):
            imm = '{:012b}'.format(int(asm2[i][2]))
        else:
            imm = '{:012b}'.format(2**12 + int(asm2[i][2]))
        inst_code.append('{:08x}'.format(int(imm + rs1 + f3[i] + rd + op[i], base=2)))

    elif(op[i] == "1100011"):
        # ******************************Branch Instructions******************************
        rs1 = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][0]].tolist()[0]]
        rs2 = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][1]].tolist()[0]]
        for x in label:
            if x[0] == asm2[i][2]:
                if x[1] >= 4*i:
                    imm = '{:012b}'.format(int((x[1] - 4*i)/2))
                else:
                    imm = '{:012b}'.format(2**12 + int((x[1] - 4*i)/2))

        inst_code.append('{:08x}'.format(int(imm[0] + imm[2:8] + rs2 + rs1 + f3[i] + imm[8:] + imm[1] + op[i], base=2)))
    
    elif(op[i] == "0000011"):
        # ******************************Load instructions******************************
        rd = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][0]].tolist()[0]]
        if(int(asm2[i][1]) >= 0):
            imm = '{:012b}'.format(int(asm2[i][1]))
        else:
            imm = '{:012b}'.format(2**12 + int(asm2[i][1]))
        rs1 = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][2]].tolist()[0]]
        inst_code.append('{:08x}'.format(int((imm + rs1 + f3[i] + rd + op[i]),base=2)))


    elif(op[i] == "0100011"):
        # ******************************Store Instructions******************************
        rs2 = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][0]].tolist()[0]]
        if(int(asm2[i][1]) >= 0):
            imm = '{:012b}'.format(int(asm2[i][1]))
        else:
            imm = '{:012b}'.format(2**12 + int(asm2[i][1]))
        rs1 = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][2]].tolist()[0]]
        inst_code.append('{:08x}'.format(int(imm[0:7] + rs2 + rs1 + f3[i] + imm[7:] + op[i], base=2)))


    elif(op[i] == "0010011"):
        # ******************************Immediate Type******************************
        rd = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][0]].tolist()[0]]
        if(int(asm2[i][2]) >= 0):
            imm = '{:012b}'.format(int(asm2[i][2]))
        else:
            imm = '{:012b}'.format(2**12 + int(asm2[i][2]))
        rs1 = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][1]].tolist()[0]]
        if(f7[i] == None):
            inst_code.append('{:08x}'.format(int((imm + rs1 + f3[i] + rd + op[i]),base=2)))
        else:
            inst_code.append('{:08x}'.format(int((f7[i] + imm[7:] + rs1 + f3[i] + rd + op[i]),base=2)))        


    elif(op[i] == "0110011"):
        # ******************************R-Type Instructions******************************
        rd = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][0]].tolist()[0]]
        rs1 = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][1]].tolist()[0]]
        rs2 = reg.regDf['value'][reg.regDf.index[reg.regDf['name'] == asm2[i][2]].tolist()[0]]
        inst_code.append('{:08x}'.format(int(f7[i] + rs2 + rs1 + f3[i] + rd + op[i], base=2)))

print(inst_code)

# things = os.listdir('.')

# print(things,type(things))
# print(os.name)

file = open('hex1.txt','w')
for x in inst_code:
    file.write(x)
    file.write("\n")
file.close()