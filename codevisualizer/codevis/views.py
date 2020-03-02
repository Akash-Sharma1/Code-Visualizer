from django.shortcuts import render

def index(request):
    if request.method=='POST':
        code = request.POST['code']
        num = int( request.POST['num'] ) # no of arrays to be tracked
        
        arrays = []# name of arrays to be tracked

        for i in range(num):
            arr = request.POST[str(i)]
            arrays.append(arr) 
        
         
        
        final=""       
        f = open(r"codevis/static/demofile.js", "w")
        f.write(final)
        f.close()
            
        return render(request,'codevis/show.html')
    return render(request, 'codevis/index.html',{})