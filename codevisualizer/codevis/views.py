from django.shortcuts import render

def index(request):
    if request.method=='POST':
        code = request.POST['code']
        num = int( request.POST['num'] ) # no of arrays to be tracked
        lang = request.POST['lang']
        arrays = []# name of arrays to be tracked
        
        #code for commenting cout on code recieved
        
        fo = open("codevis/code intercepted/source.cpp","w")
        ln = code.splitlines(True)
        final=""
        for i in range(len(ln)):
            t = ln[i].find("cout")
            if t != -1:
                temp = ln[i][:t] + "//"
                t2 = ln[i][t:].find(';')
                if(t2 != -1):
                    temp += ln[i][t:t+t2+1] + '\n'
                    ln.insert(i+1,ln[i][t+t2+1:])
                ln[i] = temp
                #i = i[:t] + "//" + i[t:]
            final+=ln[i]+'\n'
        
        
        
        for i in range(num):
            arr = request.POST[str(i)]
            arrays.append(arr) 
        
        subprocess.call(["g++","codevis//code intercepted//source.cpp"])
        subprocess.call("codevis//code intercepted//a.exe")
            
        return render(request,'codevis/show.html')
    return render(request, 'codevis/index.html',{})
