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