#include <iostream>
#include <fstream>

int main()
{
	const char* input_data="Let's begin:";
	std::ofstream outfile;
	outfile.open("tmp.txt",std::ios::app);
	outfile<<input_data<<std::endl;
	std::cout<<"Writing succeeded!\n";
	char input_again[20];
	std::cout<<"Type your information needed to write into files:"<<std::endl;
	std::cin.getline(input_again,20);	
	outfile<<input_again<<std::endl;
	std::cout<<"Writing succeeded!\n";
	outfile.close();

	char read_result[100];
	std::ifstream infile;
	infile.open("tmp.txt");
	infile>>read_result;
	std::cout<<read_result<<std::endl;
	infile.close();

	std::cin.get();
	return 0;
}
