int visuals_count;
#define print_visuals(arr)visuals_count=0;for(auto visuals_element:arr){visuals_count++;}cout<<" "<<visuals_count<<endl;for(auto visuals_element:arr){cout<<visuals_element<<" ";}cout<<endl;
#include<bits/stdc++.h>
using namespace std;
  int arr[10];
int brr[10];
int main(){freopen("output1.txt","w",stdout);
arr[0]=2; cout<<"arr";print_visuals(arr); cout<<"brr";print_visuals(brr);cout<<-1<<endl<<-1<<endl;
arr[4]=2; cout<<"arr";print_visuals(arr); cout<<"brr";print_visuals(brr);cout<<-1<<endl<<-1<<endl;
for(int i=0; i < 5;i++){
arr[i]=5; cout<<"arr";print_visuals(arr); cout<<"brr";print_visuals(brr);cout<<-1<<endl<<-1<<endl;
//arr[i]=-5;
//cout<<arr[i]<<endl;
arr[i]=i*3; cout<<"arr";print_visuals(arr); cout<<"brr";print_visuals(brr);cout<<-1<<endl<<-1<<endl;
int x=9; cout<<"arr";print_visuals(arr); cout<<"brr";print_visuals(brr);cout<<-1<<endl<<-1<<endl;
arr[i]+=5; cout<<"arr";print_visuals(arr); cout<<"brr";print_visuals(brr);cout<<-1<<endl<<-1<<endl;
}
}
