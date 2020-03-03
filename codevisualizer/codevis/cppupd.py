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
    if code[i] in symbols:
        return "-1"
    while(i < len(code)):
        if alpha(code[i]):
            final+=code[i]
        else:
            break
        i+=1
    if final in arrays:
        return final
    return "-1"


def is_valid_variable(a,b,symbols):
    if a in symbols and b in symbols:
        return True
    return False

def alpha(i):
    if (ord(i)>=97 and ord(i)<97+26) or (ord(i)>=65 and ord(i)<65+26) or (ord(i)>=48 and ord(i)<48+10):
        return True
    return False

def checkarrays(code,arrays):
    dic = ["0"]*len(code)
    symbols = [' ', '\n', ';', '<', '>', ',', '.', '(' ,')', '{' ,'}', '[' , ']', '+', '*', '-', '/', '^', '=', '&', '%' ,'!', '|' ,]
    for i in range(len(code)):
        x = sub_inarray(code,arrays,i,symbols)
        if x!="-1":
            if is_valid_variable(code[i-1],code[i+len(x)],symbols):
                dic[i]=x
                #potential out of bound
    return dic

def checkupdates(code,dic):
    for i in range(len(code)):
        if dic[i] != "0":
            flag="0"
            j=i
            while(j < len(code) and j!='\n' and j!=';'):
                if code[j]=='=' or code[j]=='.':
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
        if y==len(final):
            #check if (){ is there
            j=x
            while(j<len(code) and code[j]==' '):
                j+=1#extra space
            if code[j]!='(':
                continue
            
            j+=1
            while j<len(code) and (alpha(code[j]) or code[j]==','):
                j+=1#args
            if code[j]!=')':
                continue
            j+=1
            while j<len(code) and (code[j]==' ' or code[j]==';'):
                j+=1#extra space
            if(code[j]!='{'):
                continue
            j+=1
            return code[0:j]+"\nfreopen(\"output.txt\",\"w\",stdout);\n"+code[j+1:len(code)]
    return "-1"
    #code doeas not contains a "int main ( ) {", hence error should be returned

def gen_define():
    final=""
    final+="#define print_visuals(arr) int visuals_count=0;"
    final+="for(int visuals_element=0;visuals_element<10;visuals_element++)"
    final+="{visuals_count++;}cout<<\" \"<<visuals_count<<endl;"
    final+="for(int visuals_element=0;visuals_element<10;visuals_element++){"
    final+="cout<<arr[visuals_element]<<\" \";}cout<<endl;"
    final+="\n"            
    return final
  
def gen_update(arr):
    return "cout<<\""+arr+"\";\nprint_visuals("+arr+");\n\n"
  
def insert_update_statements(code,dic):
    final=""
    i=0
    while i < len(code):
        if dic[i]!="0":
            j=i
            while j<len(code) and code[j]!=';' and code[j]!='\n':
                final+=code[j]
                j+=1
            if j < len(code) and code[j]==';':
                final+=code[j]
                j+=1
            if j<len(code) and code[j]=='\n':
                final+=code[j]
                j+=1
            final+=gen_update(dic[i])
            i=j
        else:
            final+=code[i]
            i+=1
    return final        

