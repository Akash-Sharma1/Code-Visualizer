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

def alpha(i):
    if (ord(i)>=97 and ord(i)<97+26) or (ord(i)>=65 and ord(i)<65+26) or (ord(i)>=48 and ord(i)<48+10):
        return True
    return False

def lines_with_semocolon(code):
    list = []
    temp=""
    for i in code:
        temp+=i
        if i=='\n':
            list.append(temp)
            temp=""
    if temp != "":
        list.append(temp)

    dic = [0]*len(list)

    idx = 0
    braces = 0
    for i in list:
        if i[0]=='/' and i[1]=='/':
            idx+=1
            continue
        for j in i:
            if j=='{':
                braces+=1
            elif j=='}':
                braces-=1
        temp=i[0:len(i)-1].strip()
        if len(temp)>0 and temp[len(temp)-1] == ';' and braces>0:
            dic[idx]=1
        idx+=1
    return (dic,list)

def add_freeopen_after_main(code,filename):
    j=index_just_after_main(code)
    if j==-1:
        return "-1"
    return code[0:j]+"freopen(\""+filename+"\",\"w\",stdout);"+code[j:len(code)]

def index_just_after_main(code):
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
            while j<len(code) and (code[j]==' ' or code[j]=='\n'):
                j+=1#extra space
            if(code[j]!='{'):
                continue
            j+=1
            return j
    return -1
    #code doeas not contains a "int main ( ) {", hence error should be returned

def gen_define():
    # final="int visuals_count;\n"
    # final+="#define print_visuals(arr) visuals_count=0;"
    # final+="for(int visuals_element=0;visuals_element<sizeof(arr)/sizeof(arr[0]);visuals_element++)"
    # final+="{visuals_count++;}cout<<\" \"<<visuals_count<<endl;"
    # final+="for(int visuals_element=0;visuals_element<sizeof(arr)/sizeof(arr[0]);visuals_element++){"
    # final+="cout<<arr[visuals_element]<<\" \";}cout<<endl;"
    # final+="\n"
    final="int visuals_count;\n"  
    final+="#define print_visuals(arr)"
    final+="visuals_count=0;"
    final+="for(auto visuals_element:arr){visuals_count++;}"
    final+="cout<<\" \""+"<<visuals_count<<endl;"
    final+="for(auto visuals_element:arr){cout<<visuals_element<<\" \";}cout<<endl;"
    final+="\n"       
    return final

def gen_update(arr):
    return " cout<<\""+arr+"\";print_visuals("+arr+");"

def insert_update_statements(code_lines,dic,arrays):
    Vsyntax=""
    for i in arrays:
        Vsyntax+=gen_update(i)
    Vsyntax+="cout<<-1<<endl<<-1<<endl;"
    final=""
    L=0
    for i in code_lines:
        L+=1
        final+=i[0:len(i)-1]
        if dic[L-1] == 1:
            final+=Vsyntax
        final+="\n"
    return final

def makeline_seq(code_lines,dic):
    final=""
    L=0
    for i in code_lines:
        L+=1
        final+=i[0:len(i)-1]
        if dic[L-1] == 1:
            final+="  cout<<"+str(L)+"<<endl;"
        final+="\n"
    return final