def correct_formatting(code):
    ln = code.splitlines(True)
    finalCode = ""
    i = 0
    while i < len(ln):
        brack = 0
        temp = ln[i]
        textPresent = False
        altered = False
        text = temp.strip()
        if(len(text) == 0):
            i+=1
            continue
        for j in range(len(temp)):
            if temp[j].isalnum():
                textPresent = True
            if temp[j] == '(':
                brack+=1
            elif temp[j] == ')':
                brack-=1
            elif temp[j] == ';':
                if brack != 0:
                    continue
                ln.insert(i+1,temp[j+1:])
                altered = True
                temp = temp[:j+1]
                break
            elif temp[j] == '/' and textPresent and j < len(temp)-1 and temp[j+1] == '/':
                ln.insert(i+1,temp[j:])
                altered = True
                temp = temp[:j]
                break
            elif temp[j] == '/' and textPresent == False and j < len(temp)-1 and temp[j+1] == '/':
                break
        finalCode+=temp
        if altered:
            finalCode+= '\n'
        i+=1
    #fo = open("codevis/code intercepted/test.cpp",'w')
    #fo.write(finalCode)
    return finalCode

def format_loops(code):
    ln = code.splitlines(True)
    finalCode = ""
    i = 0
    #print(len(ln))
    cnt = 0
    while i < len(ln):
        temp = ln[i]
        temp2 = temp.strip()
        if temp2[0] == '/' and len(temp2) > 1 and temp2[1] == '/':
            finalCode+=temp
            i+=1
            continue
        if "for" in temp:
            ini = temp.find("for")
            j = ini + 3
            temp = temp[:j] + temp[j:].strip()
            if temp[j] == '(':
                while temp[j] != ')':
                    j+=1
                temp2 = temp[j+1:].strip()
                if(len(temp2) == 0):
                    bracePresent = True
                    for p in range(i+1,len(ln)):
                        if len(ln[p].strip()) != 0:
                            if ln[p].strip().find('{') != 0:
                                bracePresent = False
                            break
                    if bracePresent == False:
                        temp = temp[:j+1] + "\n{\n"
                        cnt+=1
                else:
                    if temp2[0] != '{':
                        ln.insert(i+1,temp[j+1:])
                        temp = temp[:j+1] + "\n{\n"
                        cnt+=1
                    else:
                        temp+='\n'

        elif "while" in temp:
            ini = temp.find("while")
            j = ini + 5
            temp = temp[:j] + temp[j:].strip()
            if temp[j] == '(':
                print("HI")
                while temp[j] != ')':
                    j+=1
                temp2 = temp[j+1:].strip()
                if(len(temp2) == 0):
                    bracePresent = True
                    for p in range(i+1,len(ln)):
                        if len(ln[p].strip()) != 0:
                            if ln[p].strip().find('{') != 0:
                                bracePresent = False
                            break
                    if bracePresent == False:
                        temp = temp[:j+1] + "\n{\n"
                        cnt+=1
                else:
                    if temp2[0] != '{':
                        ln.insert(i+1,temp[j+1:])
                        temp = temp[:j+1] + "\n{\n"
                        cnt+=1
                    else:
                        temp+='\n'

        elif cnt != 0:
            j = temp.find(';')
            if j != -1:
                temp = temp[:j+1] + '\n}'*cnt +'\n'+ temp[j+1:]
                cnt = 0
        finalCode += temp
        i+=1
    #print(finalCode)
    return finalCode