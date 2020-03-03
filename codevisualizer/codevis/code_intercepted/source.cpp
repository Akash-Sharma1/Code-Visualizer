int visuals_count;
#define print_visuals(arr)visuals_count=0;for(auto visuals_element:arr){visuals_count++;}cout<<" "<<visuals_count<<endl;for(auto visuals_element:arr){cout<<visuals_element<<" ";}cout<<endl;
#include<bits/stdc++.h>
using namespace std;
int main(){
freopen("output.txt","w",stdout);
int arr[10]={0};
cout<<"arr";
print_visuals(arr);

int brr[20]={1};
cout<<"brr";
print_visuals(brr);

for(int i=0;i<10;i++){
   brr[i]=i+1;
cout<<"brr";
print_visuals(brr);

   arr[i]=3;
cout<<"arr";
print_visuals(arr);

}
}