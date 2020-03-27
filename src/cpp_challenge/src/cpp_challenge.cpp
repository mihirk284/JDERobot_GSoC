#include <bits/stdc++.h>
#include <fstream>
#include <iostream>

using namespace std;



int visited[100][100], data[100][100], result[100][100];
vector<pair<int, int> > temp_order, max_order;

int del_x[] = {1, 0, -1, 0};
int del_y[] = {0, 1, 0, -1};

int rows= 0, cols =  0;
int depth = 0, max_depth = INT_MIN;

bool check_valid(int x, int y)
{
    return (x < rows && x >=0 && y < cols && y >=0);
}

void dfs(int i, int j, int depth)
{
    visited[i][j] = 1;
    for(int k = 0; k < 4; k++)
    {
        int x = i + del_x[k];
        int y = j + del_y[k];

        if (check_valid(x,y) && visited[x][y] == 0 && data[x][y] == 1 )
        {
            temp_order.push_back(make_pair(x,y));
            
            if(max_depth < (depth + 1))
            {
                max_depth = depth + 1;
                max_order = temp_order;
            }
            dfs(x,y, depth + 1);
            temp_order.pop_back();
            visited[x][y] = 0;
        }
    }
}

int main()
{

    char filepath[100];
    ifstream infile("input.txt");
    string line;
    vector<string> vec;
    int linectr = 0;
    cout << "Starting to read"<<endl;
    while(getline(infile, line))
    {
        if(linectr == 0)
            cols = line.length();
        vec.push_back(line);
        for(int i = 0; i< line.length(); i++)
        {
            if (line[i] == '.')
            {
                data[linectr][i] = 1;
            }
            else
            {
                data[linectr][i] = 0;
            }
        }
        //cout << line << endl;
        linectr++;
    }
    cout << "FINISHED READING"<<endl;
    rows = linectr;

    int mx = INT_MIN;
    for(int i = 0; i < rows; i++)
    {
        for(int j = 0; j < cols; j++)
        {
            temp_order.clear();
            if(visited[i][j] == 0 && data[i][j] == 1)
            {
                depth = 0;
                temp_order.push_back(make_pair(i,j));
                dfs(i,j,depth);
                temp_order.pop_back();
                

                if(max_depth > mx)
                {
                    mx = max_depth;
                }
            }
        }
    }
    cout<< max_depth+1 << endl;
    //cout << "Max order len  " << max_order.size()<<endl;
    int depth = 0;
    for(vector< pair<int,int> >::iterator k = max_order.begin(); k!= max_order.end(); k++)
    {
        vec[k->first][k->second] = char(depth+48);
        depth++;
    }
    for(vector< string>::iterator k = vec.begin(); k!= vec.end(); k++)
    {

        cout << *k<<endl;
    }



}



