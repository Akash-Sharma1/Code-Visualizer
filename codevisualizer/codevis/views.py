from django.shortcuts import render,HttpResponse
import os
from . import cppupd,cppformat

def change_cpp(code,arrays):
    code = code.replace('\r','')
    code=cppupd.comment_cout(code)#code for commenting cout on code recieved
    (flag_lines,code_lines) = cppupd.lines_with_semocolon(code)
    
    #print(code_lines)
    code2 = cppupd.makeline_seq(code_lines,flag_lines)#puts line no after the lines
    #print(code2)
    code2=cppupd.add_freeopen_after_main(code2,"output2.txt")#changes ordering of dic
    
    code1=cppupd.insert_update_statements(code_lines,flag_lines,arrays)#puts the visual syntax at end of lines
    code1=cppupd.gen_define()+code1
    code1=cppupd.add_freeopen_after_main(code1,"output1.txt")#changes ordering of dic
    # if function returned "-1" then code doesn't contains a "int main(){"
    return (code1,code2,flag_lines)

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
            code = cppformat.correct_formatting(code) #separate semicolons with new lines, puts comments in new line
            code = cppformat.format_loops(code) #add braces to loops
            # print(code)
            (code1,code2,flag_lines) = change_cpp(code,arrays)
            
            # return HttpResponse("ok")
            gen_source_cpp(code1,"source1.cpp")
            Updated=read_output1()
            gen_source_cpp(code2,"source2.cpp")
            line_seq=read_output2()
        
            if ( len(Updated)==0 and len(line_seq) == 0 ) or ( code1=="-1" ):
                return HttpResponse("Compilation error / Nothing to Show")
        
            final={
                'out': Updated,# printed arrays
                'flag_lines': flag_lines,#array of 0/1
                'len_arr': len(arrays),#distinct arrays
                'arrays': arrays,#all traced arrays
                'code': code,# side pane code
                'line_seq': line_seq,
            }    
            # fo = open ("output2.txt","w")
            # fo.write("")
            # fo.close
            # fo = open ("output1.txt","w")
            # fo.write("")
            # fo.close
        return render(request,'codevis/show.html',final)
    return render(request, 'codevis/index.html',{})

def read_output1():
    fo = open ("output1.txt","r")
    lines=fo.readlines()
    fo.close()
    Updates=[]
    for num in range(0,len(lines),2):
        line1 = lines[num].split()
        if line1[0] != '-1':
            array_name = line1[0].strip()
            array_size = line1[1].strip()
            array_elem = []
            if int(array_size) > 0 and num+1<len(lines):
                line2 = lines[num+1].split()
                for i in line2:
                    array_elem.append(i.strip())
            Updates.append({
                'arr_name': array_name,
                'arr_size': array_size,
                'arr_elem': array_elem, 
            })
        else:
            Updates.append({
                'arr_name': '-1',
                'arr_size': '-1',
                'arr_elem': ['-1'], 
            })
    return Updates
    
def read_output2():
    fo = open ("output2.txt","r")
    lines=fo.readlines()
    fo.close()
    line_seq=[]
    for num in lines:
        line_seq.append(num.strip())
    return line_seq
    
def gen_source_cpp(code,filename):
    fo = open("codevis\code_intercepted\\"+filename,"w")
    fo.write(code)
    fo.close()
    os.system("g++ -o codevis\\code_intercepted\\a codevis\\code_intercepted\\"+filename)
    os.system("codevis\\code_intercepted\\a.exe")
