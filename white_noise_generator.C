//white noise generator

#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <fstream>
using namespace std;

void white_noise_generator() {
    srand(time(NULL));
    Double_t value=0.0;
    Double_t time=0.0;
    Double_t T=5000.; // total data acquisition time in Sec
    Int_t max=100000;
    ofstream myfile;
    myfile.open ("white_noise2.csv");
	for (Int_t i = 1; i <=max; ++i) {
	  //value = rand()%2;
	  time=(double)i*T/max;
	  value=((double) rand() / (RAND_MAX)*0.1)+0.1;
	  myfile << time << " " << value << " " << 2*value <<" "<< 3*value << " " << 4*value<< endl;
	  //cout << value << endl;
	}
	myfile.close();
      }
