#define print_visuals(arr) int visuals_count=0;for(int visuals_element=0;visuals_element<10;visuals_element++){visuals_count++;}cout<<" "<<visuals_count<<endl;for(int visuals_element=0;visuals_element<10;visuals_element++){cout<<arr[visuals_element]<<" ";}cout<<endl;
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