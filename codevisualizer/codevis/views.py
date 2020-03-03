from django.shortcuts import render

def comment_cout(code):
    ln = code.splitlines(True)
    final = ""
    i = 0
    while i < len(ln):
        t = ln[i].find("cout")
        if t != -1:
            temp = ln[i][:t] + "//"
            t2 = ln[i][t:].find(';')
            if(t2 != -1):
                temp += ln[i][t:t+t2+1]
                ln.insert(i+1,ln[i][t+t2+1:])
            ln[i] = temp
            #i = i[:t] + "//" + i[t:]
        final += ln[i]
        #fo.write(ln[i])
        i+=1
    return final

def sub_inarray(code,arrays,i,symbols):
    final=""
    while(i < len(code)):
        if code[i] in symbols:
            break
        else:
            final+=code[i]
        i+=1
    if final in arrays:
        return final
    return "-1"


def is_valid_variable(a,b,symbols):
    if a in symbols and b in symbols:
        return True
    return False

def checkarrays(code,arrays):
    dic = ["0"]*len(code)
    symbols = [' ', '\n', ';', '<', '>', ',', '.', '(' ,')', '{' ,'}', '[' , ']', '+', '*', '-', '/', '^', '=', '&', '%' ,'!', '|' ,]
    for i in range(len(code)):
        x = sub_inarray(code,arrays,i,symbols)
        if x!="-1":
            if is_valid_variable(code[i-1],code[i+x],symbols):
                dic[i]=x
                #potential out of bound
    return dic

def checkupdates(code,dic):
    for i in range(len(code)):
        if dic[i] != "0":
            flag="0"
            j=i
            while(j < len(code) and j!='\n' and j!=';'):
                if j=='=' or j=='.':
                    flag=dic[i]
                j+=1
                #potential == failure case
            dic[i]=flag
    return dic

def add_freeopen_after_main(code):
    for i in range(len(code)):
        final="int main"
        x=i
        y=0
        while(x<len(code) and y<len(final) and final[y]==code[x]):
            x+=1
            y+=1
        if y==8:
            #check if (){ is there
            j=i
            while(j<len(code) and code[j]==' '):
                j+=1#extra space
            if code[j]!='(':
                continue
            j+=1
            while j<len(code) and ( (ord(code[j])>=97 and ord(code[j])<97+26) or (ord(code[j])>=48 and ord(code[j])<48+10) or code[i]==','):
                j+=1#args
            if code[j]!=')':
                continue
            j+=1
            while j<len(code) and (code[j]==' ' or code[j]==';'):
                j+=1#extra space
            if(code[j]!='{'):
                continue
            j+=1
            return code[0:j]+"\nfreopen(\"codevis/code intercepted/output.txt\",\"w\",stdout);\nint lenzz=0;\n"+code[j+1:len(code)]
    return "-1"
    #code doeas not contains a "int main ( ) {", hence error should be returned

def gen_update(arr):
    final="\nint lenzz=0;\n"
    final+="for(auto i:"+arr+"){lenzz++;}\n"
    final+="cout<<"+arr+"<<\" \""+"lenzz<<endl;\n"
    final+="for(auto i:"+arr+"){cout<<"+arr+"[i]<<\" \";}"            
    return final

def insert_update_statements(code,dic):
    final=""
    i=0
    while i < len(code):
        if dic[i]!="0":
            j=i
            while j<len(code) and code[j]!=';' and code[j]!="\n":
                final+=code[j]
                j+=1
            if j < len(code):
                final+=code[j]
                j+=1
            final+=gen_update(dic[i])
            i=j
        else:
            final+=code[i]
            i+=1
    return final         



def index(request):
    if request.method=='POST':
        code = request.POST['code']
        num = int( request.POST['num'] ) # no of arrays to be tracked
        lang = request.POST['lang']
        arrays = []# name of arrays to be tracked
        
        for i in range(num):
            arr = request.POST[str(i)]
            arrays.append(arr) 
            
        #code for commenting cout on code recieved
        code=comment_cout(code)
        
        #valid index of arrays in code which are upadting will have 1 in the dic
        dic = checkarrays(code,arrays)
        dic = checkupdates(code,dic)
        
        code=add_freeopen_after_main(code)
        #if function returned "-1" then code doesn't contains a "int main(){"
        
        code=insert_update_statements(code,dic)
         
        fo = open("codevis/code intercepted/source.cpp","w")
        fo.write(code)
        subprocess.call(["g++","codevis//code intercepted//source.cpp"])
        subprocess.call("codevis//code intercepted//a.exe")
        return render(request,'codevis/show.html')
    return render(request, 'codevis/index.html',{})