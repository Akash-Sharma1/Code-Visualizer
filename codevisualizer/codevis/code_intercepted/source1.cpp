int visuals_count;
#define print_visuals(arr)visuals_count=0;for(auto visuals_element:arr){visuals_count++;}cout<<" "<<visuals_count<<endl;for(auto visuals_element:arr){cout<<visuals_element<<" ";}cout<<endl;
#include <bits/stdc++.h>
using namespace std;
int main() {freopen("output1.txt","w",stdout);
int arr[10]={0};  cout<<"arr";print_visuals(arr);

int brr[10]={0};  cout<<"brr";print_visuals(brr);

int a=0;
int b=0;
int c=0;
for(int i=0;i<10;i++){
//cout<<arr[i]<<" ";  cout<<"arr";print_visuals(arr);

arr[i]=i*72+1;  cout<<"arr";print_visuals(arr);

arr[i]+=1;  cout<<"arr";print_visuals(arr);

}
a=7;
b=8;
for(int i=0;i<10;i++){
//cout<<arr[i]<<" ";  cout<<"arr";print_visuals(arr);

brr[i]=arr[i]*72+1;  cout<<"brr";print_visuals(brr);

}
}