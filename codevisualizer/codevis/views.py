from django.shortcuts import render,HttpResponse
import os
from . import cppupd

def change_cpp(code,arrays):
    code = code.replace('\r','')
    code=cppupd.comment_cout(code)#code for commenting cout on code recieved
    dic = cppupd.checkarrays(code,arrays)#valid index of arrays in code which are upadting will have 1 in the dic
    dic = cppupd.checkupdates(code,dic)
    code=cppupd.insert_update_statements(code,dic)#changes ordering of dic
    code=cppupd.gen_define()+code
    code=cppupd.add_freeopen_after_main(code)#changes ordering of dic
    # if function returned "-1" then code doesn't contains a "int main(){"
    return code

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
                        temp = temp[:j+1] + "{\n"
                        cnt+=1
                else:
                    if temp2[0] != '{':
                        ln.insert(i+1,temp[j+1:])
                        temp = temp[:j+1] + "{\n"
                        cnt+=1

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
                        temp = temp[:j+1] + "{\n"
                        cnt+=1
                else:
                    if temp2[0] != '{':
                        ln.insert(i+1,temp[j+1:])
                        temp = temp[:j+1] + "{\n"
                        cnt+=1

        elif cnt != 0:
            j = temp.find(';')
            if j != -1:
                temp = temp[:j+1] + '}'*cnt +'\n'+ temp[j+1:]
                cnt = 0
        finalCode += temp
        i+=1
    #print(finalCode)

    fo = open("codevis/code intercepted/test.cpp",'w')
    fo.write(finalCode)
    return finalCode

def index(request):
    if request.method=='POST':
        code = request.POST['code']
        num = int( request.POST['num'] ) #no of arrays to be tracked
        lang = request.POST['lang']
        arrays = [] #name of arrays to be tracked
        for i in range(num):
            arr = request.POST[str(i)]
            if arr == "":
                continue
            arrays.append(arr) 

        if lang=="C++":
            code = correct_formatting(code) #separate semicolons with new lines, puts comments in new line
            code = format_loops(code) #add braces to loops
            code = change_cpp(code,arrays)
            if code=="-1":
                return HttpResponse("Invalid code")
            
            fo = open("codevis\code_intercepted\source.cpp","w")
            fo.write(code)
            fo.close()
            
            os.system("g++ -o codevis\\code_intercepted\\a codevis\\code_intercepted\\source.cpp")
            os.system("codevis\\code_intercepted\\a.exe")
            
        fo = open ("output.txt","r")
        lines=fo.readlines()
        
        final=[]
        for num in range(0,len(lines),2):
            line1 = lines[num].split()
            line2 = lines[num+1].split()
            array_name = line1[0].strip()
            array_size = line1[0].strip()
            array_elem=[]
            for i in line2:
                array_elem.append(i.strip())
            final.append({
                'arr_name': array_name,
                'arr_size': array_size,
                'arr_elem': array_elem, 
            })
            
        return render(request,'codevis/show.html',{'out':final})
    return render(request, 'codevis/index.html',{})

# #include <bits/stdc++.h>
# using namespace std;
# int main(){
#     int arr[10]={0};
#     for(int i=0;i<10;i++){
#         arr[i]=1;
#     }
# }