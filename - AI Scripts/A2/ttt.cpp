# include <iostream>
# include <string>
# include <vector>

using namespace std;

bool pruning = true;
int nodes = 0;
// int alpha_v = -10;
// int beta_v = 10;

class Board {
    public:
    vector<vector<char>> board;
    int depth;
    float alpha, beta;

    Board(){
        board = {{'.','.','.'},{'.','.','.'},{'.','.','.'}};
        depth = 0;
        alpha = -10.0;
        beta = 10.0;
    }

    void show(){
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                cout<<' '<<board[i][j];
            }
            cout<<endl;
        }
    }

    void reset(){
        board = {{'.','.','.'},{'.','.','.'},{'.','.','.'}};
    }

    float score(char piece){
        char opp;
        if(piece == 'X'){
            opp = 'O';
        } else {
            opp = 'X';
        }
        // wins
        if(board[0][0]==piece&&board[0][1]==piece&&board[0][2]==piece){
            return 1 - 0.1 * depth;
        }
        if(board[1][0]==piece&&board[1][1]==piece&&board[1][2]==piece){
            return 1 - 0.1 * depth;
        }
        if(board[2][0]==piece&&board[2][1]==piece&&board[2][2]==piece){
            return 1 - 0.1 * depth;
        }
        if(board[0][0]==piece&&board[1][0]==piece&&board[2][0]==piece){
            return 1 - 0.1 * depth;
        }
        if(board[0][1]==piece&&board[1][1]==piece&&board[2][1]==piece){
            return 1 - 0.1 * depth;
        }
        if(board[0][2]==piece&&board[1][2]==piece&&board[2][2]==piece){
            return 1 - 0.1 * depth;
        }
        if(board[0][0]==piece&&board[1][1]==piece&&board[2][2]==piece){
            return 1 - 0.1 * depth;
        }
        if(board[0][2]==piece&&board[1][1]==piece&&board[2][0]==piece){
            return 1 - 0.1 * depth;
        }
        // losses
        if(board[0][0]==opp&&board[0][1]==opp&&board[0][2]==opp){
            return -1 + 0.1 * depth;
        }
        if(board[1][0]==opp&&board[1][1]==opp&&board[1][2]==opp){
            return -1 + 0.1 * depth;
        }
        if(board[2][0]==opp&&board[2][1]==opp&&board[2][2]==opp){
            return -1 + 0.1 * depth;
        }
        if(board[0][0]==opp&&board[1][0]==opp&&board[2][0]==opp){
            return -1 + 0.1 * depth;
        }
        if(board[0][1]==opp&&board[1][1]==opp&&board[2][1]==opp){
            return -1 + 0.1 * depth;
        }
        if(board[0][2]==opp&&board[1][2]==opp&&board[2][2]==opp){
            return -1 + 0.1 * depth;
        }
        if(board[0][0]==opp&&board[1][1]==opp&&board[2][2]==opp){
            return -1 + 0.1 * depth;
        }
        if(board[0][2]==opp&&board[1][1]==opp&&board[2][0]==opp){
            return -1 + 0.1 * depth;
        }
        // draw
        return 0;
    }

    int count_blank(){
        int count = 0;
        for(int i=0;i<3;i++){
            for(int j=0;j<3;j++){
                if(board[i][j]=='.'){
                    count++;
                }
            }
        }
        return count;
    }

    void check_over(){
        if(count_blank()==0){
            if(score('X')==0){
                cout << "Draw" << endl;
            }
        }
        if(score('X')>0){
            cout << "X Wins!" << endl;
        }
        if(score('O')>0){
            cout << "O Wins!" << endl;
        }
    }

    Board(const Board& a){
        board = a.board;
        depth = a.depth;
        alpha = a.alpha;
        beta = a.beta;
    }
};

void move(char piece, char r, int col, Board &board){
    int row;
    col=col-49;
    switch (r){
    case 'A':
        row = 0;
        break;
    case 'B':
        row = 1;
        break;
    case 'C':
        row = 2;
        break;
    }
    board.board[row][col] = piece;
}



float maxi(char piece, Board &board);
float mini(char piece, Board &board);

void minimax(char piece, Board &board){
    board.depth = 9-board.count_blank();
    Board test = board;
    // cout << test.board[0][0]<<endl;
    int x,y = 0;
    char opp;
    if(piece == 'X'){
        opp = 'O';
    } else {
        opp = 'X';
    }
    char c;
    Board max;
    float score = -10;
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            if (test.board[i][j]=='.'){
                test.board[i][j]=piece;
                nodes++;
                test.depth++;
                float num = mini(piece, test);
                switch (i)
                {
                case 0:
                    c='A';
                    break;
                case 1:
                    c='B';
                    break;
                case 2:
                    c='C';
                    break;
                }
                cout<<"move ("<<c<<","<<j+1<<") mm-score: "<<num<<endl;
                if (num>score){
                    // cout << "found minimax:"<<i<<","<<j<<endl;
                    score = num;
                    max = board;
                    max.board[i][j]=piece;
                }
                test=board;
            }
        }
    }
    cout<<"number of nodes searched: "<< nodes<<endl;
    nodes=0;
    board = max;
    // alpha_v=-10;
    // beta_v=10;
}

float mini(char piece, Board &board){
    board.depth = 9-board.count_blank();
    if(board.count_blank()==0){
        float s = board.score(piece);
        board.alpha=s;
        board.beta=s;
        return s;
    }
    char opp;
    if(piece == 'X'){
        opp = 'O';
    } else {
        opp = 'X';
    }
    Board test = board;
    Board max = board;
    float score=10;
    int a = board.alpha;
    int b = 10;
    if(board.score(piece) != 0){
        float s = board.score(piece);
        if(board.beta>s){
            board.alpha=s;
            board.beta=s;
        }
        return s;
    }
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            if(b<=board.alpha && pruning){
                // cout<<"working!"<< endl;
                return -10;
            }
            if(test.board[i][j]=='.'){
                test.board[i][j]=opp;
                nodes++;
                test.depth++;
                test.beta=b;
                float num = maxi(piece, test);
                if(num<score){
                    max=board;
                    // cout << "found min" << endl;
                    b=num;
                    max.board[i][j]=opp;
                    score=num;
                }
                test=board;
            }
        }
    }
    board=max;
    if(b>board.alpha){
        board.alpha=b;
    }
    return score;
}

float maxi(char piece, Board &board){
    board.depth = 9-board.count_blank();
    if(board.count_blank()==0){
        float s = board.score(piece);
        if(board.alpha<s){
            board.alpha=s;
            board.beta=s;
        }
        return s;
    }
    char opp;
    if(piece == 'X'){
        opp = 'O';
    } else {
        opp = 'X';
    }
    Board test = board;
    Board min = board;
    float score= -10;
    int a = -10;
    int b = board.beta;
    if(board.score(piece) != 0){
        float s = board.score(piece);
        board.alpha=s;
        board.beta=s;
        return s;
    }
    for(int i=0;i<3;i++){
        for(int j=0;j<3;j++){
            if(a>=board.beta && pruning){
                // cout<<"working!"<< endl;
                return 10;
            }
            if(test.board[i][j]=='.'){
                test.board[i][j]=piece;
                nodes++;
                test.depth++;
                test.alpha=a;
                float num = mini(piece, test);
                if(num>score){
                    min = board;
                    // cout << "found max"<< endl;
                    a=num;
                    min.board[i][j]=piece;
                    score=num;
                }
                test=board;
            }
        }
    }
    board = min;
    if(a<board.beta){
        board.beta=a;
    }
    return score;
}

int main () {
    Board board;
    string input;
    board.show();
    while(getline(cin,input)){
        if(input=="show"){
            board.show();
        }
        else if(input=="reset"){
            board.reset();
            board.show();
        }
        else if(input.find("move")!=string::npos){
            if(input[5]=='X'||input[5]=='O'){
                move(input[5], input[7], input[9], board);
                board.show();
                board.check_over();
            } else {
                cout << "Invalid Input" << endl;
                board.show();
            }
        }
        else if(input=="pruning on"){
            pruning=true;
            cout<<"Pruning is on"<<endl;
            board.show();
        }
        else if(input=="pruning off"){
            pruning=false;
            cout<<"Pruning is off"<<endl;
            board.show();
        }
        else if(input=="pruning"){
            if(pruning){
                cout<<"Pruning is on"<<endl;
                board.show();
            }else{
                cout<<"Pruning is off"<<endl;
                board.show();
            }
        }
        else if(input=="quit"){
            cout<<"Thanks for Playing!"<<endl;
            break;
        }else if(input.find("choose")!=string::npos) {
            minimax(input[7],board);
            board.show();
            board.check_over();
        }else{
            cout << "Invalid Input" << endl;
            board.show();
        }
    }
    return 0;
}