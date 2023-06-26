#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <string.h>
using namespace std;

int main(){
    vector<vector<string>> node = {{"WA","NT","SA"},{"NT","WA","SA","Q"},{"SA","WA","NT","Q","NSW","V"},{"Q","NT","SA","NSW"},{"NSW","SA","Q","V"},{"V","SA","NSW"}};
    vector<string> color = {"R","G","B"};
    ofstream f ("mapcolor.cnf");
    for(int i=0;i<node.size();i++){
        for(int j=0;j<color.size();j++){
            f<<node[i][0]<<color[j]<<" ";
        }
        f<<endl;
    }
    for(int i=0;i<node.size();i++){
        f<<"-"<<node[i][0]<<"R "<<"-"<<node[i][0]<<"G "<<endl;
        f<<"-"<<node[i][0]<<"R "<<"-"<<node[i][0]<<"B "<<endl;
        f<<"-"<<node[i][0]<<"B "<<"-"<<node[i][0]<<"G "<<endl;
    }
    for(int i=0;i<node.size();i++){
        for(int k=0;k<color.size();k++){
            for(int j=1;j<node[i].size();j++){
                f<<"-"<<node[i][0]<<color[k]<<" "<<"-"<<node[i][j]<<color[k]<<endl;
            }
        }
    }
    f.close();
    return 0;
}