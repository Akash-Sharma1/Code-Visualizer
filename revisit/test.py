def test1(start, end):

    for num in range(start, end + 1):

        if num % 2 == 0:
            print(num, end=" ")
            print("\n")  # even numbers


def test2():
    a = 7
    b = 4
    c = 9
    b = b-1
    a = a+1
    a = b+c
    c = b-a
    b = b-1
    a = a+1
    a = b+c
    c = b-a
    b = b-1
    a = a+1
    a = b+c
    c = b-a
    for i in range(2, 10):
        for j in range(2, int(i**.5)+1):
            if i % j == 0:
                break
        else:
            print(i)
            
def main():
    # List of Integers 
    numbers = [1, 3, 4, 2] 
    
    # Sorting list of Integers 
    numbers.sort() 
    
    test2()
    #print(numbers) 
    
    # List of Floating point numbers 
    decimalnumber = [2.01, 2.00, 3.67, 3.28, 1.68] 
    
    # Sorting list of Floating point numbers 
    decimalnumber.sort() 
    
    #print(decimalnumber) 
    
    # List of strings 
    words = ["Geeks", "For", "Geeks"] 
    
    # Sorting list of strings 
    words.sort() 
    
    #print(words)