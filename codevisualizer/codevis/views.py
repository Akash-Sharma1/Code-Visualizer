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
    final=[]
    for i in range(len(dic)):
        if dic[i]!='0':
            final.append(i+1)
    return (code,final)

def index(request):
    if request.method=='POST':
        Factory_code = request.POST['code']
        num = int( request.POST['num'] ) #no of arrays to be tracked
        lang = request.POST['lang']
        arrays = [] #name of arrays to be tracked
        for i in range(num):
            arr = request.POST[str(i)]
            if arr == "":
                continue
            arrays.append(arr) 

        if lang=="C++":
            code,dic = change_cpp(Factory_code,arrays)
            if code=="-1":
                return HttpResponse("Invalid code")
            
            fo = open("codevis\code_intercepted\source.cpp","w")
            fo.write(code)
            fo.close()
            
            os.system("g++ -o codevis\\code_intercepted\\a codevis\\code_intercepted\\source.cpp")
            os.system("codevis\\code_intercepted\\a.exe")
        elif lang=="Python":
            pass
        else:
            pass
        fo = open ("output.txt","r")
        lines=fo.readlines()
        
        final=[]
        for num in range(0,len(lines),2):
            line1 = lines[num].split()
            line2 = lines[num+1].split()
            array_name = line1[0].strip()
            array_size = line1[1].strip()
            array_elem=[]
            for i in line2:
                array_elem.append(i.strip())
            final.append({
                'arr_name': array_name,
                'arr_size': array_size,
                'arr_elem': array_elem, 
            })
        fo.close()
        fo = open ("output.txt","w")
        fo.write("")
        fo.close()
        return render(request,'codevis/show.html',{'out':final,'distinct_arrays': len(arrays), 'arrays': arrays,'fac_code':Factory_code ,'dic': dic})
    return render(request, 'codevis/index.html',{})