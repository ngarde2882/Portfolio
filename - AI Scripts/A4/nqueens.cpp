#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <string.h>
using namespace std;

int main(int argc, char *argv[]){
    char n = argv[1][0];
    // cout<<n<<endl;
    string str = "queens.cnf";
    str.insert(0,1,n);
    // cout<<str<<endl;
    ofstream f (str);
    int N = (int)n-48;
    // cout<<N<<endl;
    for(int i=1;i<=N;i++){
        for(int j=1;j<=N;j++){
            f<<i<<j<<" ";
        }
        f<<endl;
    }
    for(int i=1;i<=N;i++){
        for(int j=1;j<=N;j++){
            for(int k=1;k<=N;k++){
                if(k!=j){
                    f<<"-"<<i<<j<<" "<<"-"<<i<<k<<endl;
                }
            }
        }
    }
    for(int i=1;i<=N;i++){
        for(int j=1;j<=N;j++){
            for(int k=1;k<=N;k++){
                if(i<j){
                    f<<"-"<<i<<k<<" "<<"-"<<j<<k<<endl;
                }
            }
        }
    }
    for(int i=1;i<=N;i++){
        for(int j=1;j<=N;j++){
            if(j>i){
                int diff1 = j-i;
                int diff2 = i-j;
                for(int k=1;k<=N;k++){
                    if(k+diff1<=N){
                        f<<"-"<<i<<k<<" -"<<j<<k+diff1<<endl;
                    } if(k+diff2>0){
                        f<<"-"<<i<<k<<" -"<<j<<k+diff2<<endl;
                    }
                }
            }
        }
    }
    f.close();
    return 0;
}