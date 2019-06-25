#include <iostream>
#include <sys/types.h>
#include <dirent.h>
#include <vector>
#include <string.h>
 
using namespace std;
 
void GetFileNames(string path,vector<string>& filenames)
{
    DIR *pDir;
    struct dirent* ptr;
    if(!(pDir = opendir(path.c_str())))
        return;
    while((ptr = readdir(pDir))!=0) {
        if (strcmp(ptr->d_name, ".") != 0 && strcmp(ptr->d_name, "..") != 0)
            filenames.push_back(path + "/" + ptr->d_name);
    }
    closedir(pDir);
}
 
int main() 
{
    vector<string> file_name;
    string path = "testfile";
 
    GetFileNames(path, file_name);
 
    for(int i = 0; i <file_name.size(); i++)
    {
        cout<<file_name[i]<<endl;
    }
 
    return 0;
}

/*
#include <iostream>
#include <sys/types.h>
#include <dirent.h>
#include <vector>
#include <string.h>

int main() 
{
    std::vector<std::string> file_name;
    std::string path = "testfile";
    DIR *pDir;
    struct dirent* ptr;
    if(!(pDir=opendir(path.c_str())))
    	return 1;

    while((ptr=readdir(pDir))!=0)
    {
    	if(strcmp(ptr->d_name,".")!=0 && strcmp(ptr->d_name,"..")!=0)
    		file_name.push_back(path+"/"+ptr->d_name);
    }

    closedir(pDir);

    for(int i = 0; i <file_name.size(); i++)
    {
        std::cout<<file_name[i]<<std::endl;
    }

    return 0;
}
*/
