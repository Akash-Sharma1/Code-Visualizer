from django.shortcuts import render,HttpResponse
import subprocess
from . import cppupd

def index(request):
    if request.method=='POST':
        code = request.POST['code']
        num = int( request.POST['num'] ) # no of arrays to be tracked
        lang = request.POST['lang']
        arrays = []# name of arrays to be tracked
    
        for i in range(num):
            arr = request.POST[str(i)]
            arrays.append(arr) 
            
        code = code.replace('\r','')
        #code for commenting cout on code recieved
        code=cppupd.comment_cout(code)
        
        #valid index of arrays in code which are upadting will have 1 in the dic
        dic = cppupd.checkarrays(code,arrays)
        dic = cppupd.checkupdates(code,dic)
        
        
        code=cppupd.insert_update_statements(code,dic)#changes ordering of dic
        code=cppupd.gen_define()+code
        
        code=cppupd.add_freeopen_after_main(code)#changes ordering of dic
        
        # if function returned "-1" then code doesn't contains a "int main(){"
        if code=="-1":
             return HttpResponse("Invalid code")
        
        fo = open("codevis/code intercepted/source.cpp","w")
        fo.write(code)
        try:
            subprocess.call(["g++","codevis/code intercepted/source.cpp"])
        except:
            return HttpResponse("Invalid Code")
        return render(request,'codevis/show.html')
    return render(request, 'codevis/index.html',{})

# #include <bits/stdc++.h>
# using namespace std;

# int main(){
#     int arr[10]={0};
#     for(int i=0;i<10;i++){
#         arr[i]=1;
#     }
# }