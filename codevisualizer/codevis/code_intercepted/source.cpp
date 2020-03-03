#define print_visuals(arr)int visuals_count=0;for(auto visuals_element:arr){visuals_count++;}cout<<" "<<visuals_count<<endl;for(auto visuals_element:arr){cout<<visuals_element<<" ";}cout<<endl;
#include <bits/stdc++.h>
using namespace std;

int main(){
freopen("output.txt","w",stdout);
    int array[10]={0};
cout<<"array";
print_visuals(array);

    for(int i=0;i<10;i++){
        array[i]=1;
cout<<"array";
print_visuals(array);

}   
}