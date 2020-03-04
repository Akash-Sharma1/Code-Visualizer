int visuals_count;
#define print_visuals(arr)visuals_count=0;for(auto visuals_element:arr){visuals_count++;}cout<<" "<<visuals_count<<endl;for(auto visuals_element:arr){cout<<visuals_element<<" ";}cout<<endl;
// C++ program for implementation of Bubble sort 
#include <bits/stdc++.h> 
using namespace std;
void swap(int *xp, int *yp) 
{ 
	int temp = *xp;
	*xp = *yp;
	*yp = temp;
} 
/* Function to print an array */
void printArray(int arr[], int size) 
{ 
	int i;
	for(i = 0; i < size; i++)
{
		//cout << arr[i] << " ";  cout<<"arr";print_visuals(arr);

}

	//cout << endl;
} 
// Driver code 
int main() 
{freopen("output1.txt","w",stdout);
	int arr[] = {64, 34, 25, 12, 22, 11, 90};  cout<<"arr";print_visuals(arr);

	int n = sizeof(arr)/sizeof(arr[0]);  cout<<"arr";print_visuals(arr);

	int i, j;
	for(i = 0; i < n-1; i++)
{
	// Last i elements are already in place 
	for(j = 0; j < n-i-1; j++)
{
		if (arr[j] > arr[j+1]) 
			swap(&arr[j], &arr[j+1]);  cout<<"arr";print_visuals(arr);

}
}

	//cout<<"Sorted array: \n";
	printArray(arr, n);  cout<<"arr";print_visuals(arr);

	return 0;
} 
// This code is contributed by rathbhupendra 
