#include <iostream>
#include <trantor/utils/Date.h>

using namespace std;
using namespace trantor;

int main(int argc, char* argv[]) 
{
    cout << "Trantor Now is: " << Date::now().toFormattedString(true) << endl;
    return 0;
}
