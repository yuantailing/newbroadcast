#include <iostream>
using namespace std;

class test
{
    int num;
public:
    test() {}
    test(int t)
    {
        num = t;
    }
};

int main()
{
    //Error! int *a[10] = new (int*)[10];
    //Error! int **b = new int [10][5];
    int *c = new int[10];
    //Error! int *d[10] = new int[5][10];

    test *tp = new test[5];

    delete []c;
    delete tp;
    return 0;
}

