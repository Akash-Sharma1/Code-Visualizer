// C++ program for implementation of Bubble sort 
#include <bits/stdc++.h> 
using namespace std;
void swap(int *xp, int *yp) 
{ 
	int temp = *xp;  cout<<6<<endl;
	*xp = *yp;  cout<<7<<endl;
	*yp = temp;  cout<<8<<endl;
} 
/* Function to print an array */
void printArray(int arr[], int size) 
{ 
	int i;  cout<<13<<endl;
	for(i = 0; i < size; i++)
{
		//cout << arr[i] << " ";  cout<<16<<endl;
}

	//cout << endl;  cout<<19<<endl;
} 
// Driver code 
int main() 
{freopen("output2.txt","w",stdout);
	int arr[] = {64, 34, 25, 12, 22, 11, 90};  cout<<24<<endl;
	int n = sizeof(arr)/sizeof(arr[0]);  cout<<25<<endl;
	int i, j;  cout<<26<<endl;
	for(i = 0; i < n-1; i++)
{
	// Last i elements are already in place 
	for(j = 0; j < n-i-1; j++)
{
		if (arr[j] > arr[j+1]) 
			swap(&arr[j], &arr[j+1]);  cout<<33<<endl;
}
}

	//cout<<"Sorted array: \n";  cout<<37<<endl;
	printArray(arr, n);  cout<<38<<endl;
	return 0;  cout<<39<<endl;
} 
// This code is contributed by rathbhupendra 
