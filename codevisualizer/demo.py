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
checkupdates("void bubbleSort(int arr[], int n)\n\n{")