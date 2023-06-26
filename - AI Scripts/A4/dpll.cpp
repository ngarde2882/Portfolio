#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <string.h>
using namespace std;

bool uch = true;
int dpll_calls = 0;
vector<char> nullvect = {};

// KB: -Av-BvC,-DvE,A,B,-E = [[-A,-B,C],[-D,E],[A],[B],[-E]]
// symbols: [A,B,C,D,E]
// model: init: [?,?,?,?,?] -> [T,T,T,F,F]
bool check(vector<vector<string>> clauses, vector<string> symbols, vector<char> model){
    vector<char> clauses_model(clauses.size(),'F');
    for(int i=0;i<clauses.size();i++){
        for(int j=0;j<clauses[i].size();j++){
            if(clauses[i][j][0]=='-'){
                string sym = clauses[i][j].substr(1,clauses[i][j].size()-1);
                for(int k=0;k<symbols.size();k++){
                    if(sym==symbols[k]){
                        if(model[k]=='F'||model[k]=='?'){
                            clauses_model[i]='T';
                            break;
                        }
                    }
                }
            } else {
                string sym = clauses[i][j];
                for(int k=0;k<symbols.size();k++){
                    if(sym==symbols[k]){
                        if(model[k]=='T'||model[k]=='?'){
                            clauses_model[i]='T';
                            break;
                        }
                    }
                }
            }
        }
    }
    for(int i=0;i<clauses_model.size();i++){
        if(clauses_model[i]=='F'){
            return false;
        }
    }
    return true;
}

vector<char> DPLL(vector<vector<string>> clauses, vector<string> symbols, vector<char> model){
    dpll_calls++;
    // print current model
    // for(int j=0;j<model.size();j++){
    // cout<<model[j]<<" ";
    // }cout<<endl;
    vector<char> trueBranch = model;
    vector<char> falseBranch = model;
    vector<char> out = nullvect;
    bool bolin = true;
    bolin = true;
    for(int i=0;i<falseBranch.size();i++){
        if(falseBranch[i]=='?'){
            bolin=false;
            falseBranch[i]='F';
            if(check(clauses,symbols,falseBranch)){
                falseBranch = DPLL(clauses,symbols,falseBranch);
                if(falseBranch!=nullvect){
                    return falseBranch;
                }
            } else {
                dpll_calls++;
            }
            break;
        }
    }
    if(bolin){
        return model;
    }
    for(int i=0;i<trueBranch.size();i++){
        if(trueBranch[i]=='?'){
            bolin=false;
            trueBranch[i]='T';
            if(check(clauses,symbols,trueBranch)){
                trueBranch = DPLL(clauses,symbols,trueBranch);
                if(trueBranch!=nullvect){
                    return trueBranch;
                }
            } else {
                dpll_calls++;
            }
            break;
        }
    }
    if(bolin){
        return model;
    }
    return nullvect;
}

vector<char> UnitClauseHeuristic(vector<vector<string>> clauses, vector<string> symbols, vector<char> model){
    for(int i=0;i<clauses.size();i++){
        if(clauses[i].size()==1){
            if(clauses[i][0][0]=='-'){
                string sym = clauses[i][0].substr(1,clauses[i][0].size()-1);
                for(int j=0;j<symbols.size();j++){
                    if(sym==symbols[j]){
                        model[j]='F';
                        break;
                    }
                }
            } else {
                string sym = clauses[i][0];
                for(int j=0;j<symbols.size();j++){
                    if(sym==symbols[j]){
                        model[j]='T';
                        break;
                    }
                }
            }
        }
    }
    return model;
}

int main (int argc, char *argv[]) {
    if(argc==3){
        string arg2 = argv[2];
        if(arg2.length()>3){
            if(arg2.substr(0,4)=="-UCH"){
                uch = false;
            }
        }
    }
    ifstream f (argv[1]);
    if(f.is_open()) {
        string line;
        vector<vector<string>> KB;
        vector<string> symbols;
        int i=0;
        while(!f.eof()){
            getline(f, line);
            cout<<i<<". "<<line<<endl;
            vector<string> clause;
            string word = "";
            for(char x : line){
                if(x==' '){
                    clause.push_back(word);
                    if(word[0]=='-'){
                        word=word.substr(1,word.length()-1);
                    }
                    bool bolin = true;
                    for(int j=0;j<symbols.size();j++){
                        if(symbols[j]==word){
                            bolin=false;
                        }
                    }
                    if(bolin){
                        symbols.push_back(word);
                    }
                    word = "";
                } else {
                    word += x;
                }
            }
            clause.push_back(word);
            if(word[0]=='-'){
                word=word.substr(1,word.length()-1);
            }
            bool bolin = true;
            for(int j=0;j<symbols.size();j++){
                if(symbols[j]==word){
                    bolin=false;
                }
            }
            if(bolin){
                symbols.push_back(word);
            }
            KB.push_back(clause);
            i++;
        } f.close();
        cout<<"...tracing info..."<<endl;

        // print KB
        // for(int j=0;j<KB.size();j++){
        //     for(int k=0;k<KB[j].size();k++){
        //         cout<<KB[j][k]<<" ";
        //     }
        //     cout << endl;
        // }
        // print symbols
        // for(int j=0;j<symbols.size();j++){
        //     cout<<symbols[j]<<" ";
        // }

        vector<char> model(symbols.size(),'?');

        if(uch){
            model=UnitClauseHeuristic(KB,symbols,model);
        }

        model = DPLL(KB,symbols,model);

        if(model!=nullvect){
            cout<<"success! found a model"<<endl;
            cout<<"model: ";
            for(int j=0;j<model.size();j++){
                cout<<symbols[j]<<'='<<model[j]<<' ';
            }
            cout<<endl;
            cout<<"true props: ";
            for(int j=0;j<model.size();j++){
                if(model[j]=='T'){
                    cout<<symbols[j]<<' ';
                }
            }
            cout<<endl;
            cout << "DPLL_calls: " <<dpll_calls<<endl;
        } else {
            cout<<"failure! no model found"<<endl;
            cout << "DPLL_calls: " <<dpll_calls<<endl;
        }
    } else {
        cout<<"File Error"<<endl;
    }
    return 0;
}