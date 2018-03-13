//*****************************************************************
//  This code takes data from two lock-in amplifiers. Channel X of the fluxgate
//  is connected to the top lock-in and channecl Y to the bottom lock-in.
//****************************•••••••************************************

#include <stdio.h>
#include <time.h>
#include <sys/time.h>
#include <ctype.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <getopt.h>
#include "gpib/ib.h"

#include <iostream>
#include <fstream>
using namespace std;



void strip_newline( char *str, int size )
{
    int i;

    /* remove the null terminator */
    for (  i = 0; i < size; ++i )
    {
        if ( str[i] == '\n' )
        {
            str[i] = '\0';

            /* we're done, so just exit the function by returning */
            return;
        }
    }
    /* if we get all the way to here, there must not have been a newline! */
}





int main (int argc, char *argv[])
{

  time_t startTime;
  float total_time=0;
   struct timeval t1,t2,t3;
   double elapsedtime1,elapsedtime2,t4;


  // Data read parameters
#define bufferSize 100000
   float data[bufferSize];
   int pointsToRead=bufferSize;
   int pointsRead;
  float timeout=20.0;
  int totalRead=0;


//********************************


   // GPIB stuff

  //The first Lock-In (for the coil)
  int dev;
  int board_index = 0;
  int pad = 8;
  int sad = 0;
  int send_eoi = 1;
  int eos_mode = 0;
  int status;
  struct timeval start_time, end_time;
  float elapsed_time;
  FILE *fp;
  uint8_t *buffer;
  static const unsigned long buffer_length = 1000;
  char cbuffer[1024];
  char rbuffer[1024];
  //	int i;

  char *token;
  float x,y;
  //float temperature1,temperature2,temperature3,temperature4; //this is for ROOT
  
  //The second Lock-In for the field measurement

  int dev2;
  int board_index2=0;
  int pad2=9;
  int sad2=0;
  int send_eoi2=1;
  int eos_mode2=0;
  int status2;
  char cbuffer2[1024];
  char rbuffer2[1024];
  char *token2;
  float x2,y2;
  
  // fle name generator

  time_t rawtime;
  struct tm * timeinfo;
  char filename[80];

  time (&rawtime);
  timeinfo = localtime(&rawtime);

  strftime(filename,80,"%d_%m_%Y_%I:%M:%S.txt",timeinfo);
 

  fp=fopen(filename,"w+");

    //fp=fopen(strftime+".txt","w+");
  //fp=fopen("test.txt","w+");
  printf("The file has been created\n");


  // Open the GPIB devices
  
  dev = ibdev( board_index, pad, sad, T1s, send_eoi, eos_mode );
  dev2 = ibdev( board_index2, pad2, sad2, T1s, send_eoi2, eos_mode2 );

  if( dev < 0 )
    {
      fprintf( stderr, "ibdev() failed\n" );
      fprintf( stderr, "%s\n", gpib_error_string( ThreadIberr() ) );
      return -1;
    }
if( dev2 < 0 )
    {
      fprintf( stderr, "ibdev() failed\n" );
      fprintf( stderr, "%s\n", gpib_error_string( ThreadIberr() ) );
      return -1;
    }
  printf("First Device online: board index=%i, pad=%i, sad=%i\n",
	 board_index,pad,sad);
  printf("Second Device online: board index=%i, pad=%i, sad=%i\n",
	 board_index2,pad2,sad2);


  

   gettimeofday(&t1,NULL);
   printf("t1=%lf s \n",t1.tv_sec+t1.tv_usec/1e6);


  // The loop will quit after 129600 seconds(1day and a half)
  startTime = time(NULL);
  while(time(NULL)<startTime+54000) {
    sleep(1);

     sprintf(cbuffer,"SNAP?1,2",cbuffer);
    sprintf(cbuffer2,"SNAP?1,2",cbuffer2);
  

    status = ibwrt(dev, cbuffer, strlen(cbuffer));
    status2 = ibwrt(dev2, cbuffer2, strlen(cbuffer2));

    if( status & ERR )
      {
	fprintf( stderr, "ibwrt() failed\n" );
	fprintf( stderr, "%s\n", gpib_error_string( ThreadIberr() ) );
	return -1;
      }
     if( status2 & ERR )
      {
	fprintf( stderr, "ibwrt() failed\n" );
	fprintf( stderr, "%s\n", gpib_error_string( ThreadIberr() ) );
	return -1;
      }
     
    status = ibrd( dev, rbuffer, 80 );
    status2 = ibrd( dev2, rbuffer2, 80 );

    if( status & ERR )
      {
	fprintf( stderr, "ibrd() failed\n" );
	fprintf( stderr, "%s\n", gpib_error_string( ThreadIberr() ) );
	return -1;
      }
    if( status2 & ERR )
      {
	fprintf( stderr, "ibrd() failed\n" );
	fprintf( stderr, "%s\n", gpib_error_string( ThreadIberr() ) );
	return -1;
      }
  
     //    printf("strlen %d\n",strlen(rbuffer));
    //printf("read string: %s\n", rbuffer);
    //sprintf("",rbuffer);
    strip_newline(rbuffer, 80 );
   
    //    rbuffer[0]='\0';
    //    printf("strlen %d\n",strlen(rbuffer));
    //    printf("read string: %s\n", rbuffer);
    token=strtok(rbuffer,",");
    
    //    printf("%s\n",token);
    x=strtof(token,NULL);
   
    token=strtok(NULL,",");

    //    printf("%s\n",token);
    y=strtof(token,NULL);

    // printf(rbuffer);
    //printf("%e %e\n",x,y);


    strip_newline(rbuffer2,80);
    token2=strtok(rbuffer2,",");
    x2=strtof(token2,NULL);
    token2=strtok(NULL,",");
    y2=strtof(token2,NULL);


    //printf ("x= %e ,  x2=%e\n",x,x2);

     
     gettimeofday(&t2,NULL);
    //the elapsed time in s:
    elapsedtime1=t2.tv_sec - t1.tv_sec +
       	( t2.tv_usec - t1.tv_usec ) / 1e6;
    t4=t2.tv_sec+t2.tv_usec/1e6;

 // printf("%f %f %f %f %f %e %e\n",(float)(time(NULL)-startTime),data[0],data[1],data[2],data[3],x,y);
    // printf("%lf s %f %f %f %f %e %e\n",elapsedtime1,data[0],data[1],data[2],data[3],x,y);
    printf("%lf s %e %e %e %e\n",t4,x,y,x2,y2);
    //  printf("%lf ms\n ",elapsedtime1);

 // fprintf(fp,"%lf %f %f %f %f %e %e\n",elapsedtime1,data[0],data[1],data[2],data[3],x,y);
    fprintf(fp,"%lf %e %e %e %e\n",t4,x,y,x2,y2);

  }

  gettimeofday(&t3,NULL);
  elapsedtime2=(t3.tv_sec-t1.tv_sec) ;

   printf("Total Time=%lf Seconds",elapsedtime2);
   //printf("\nAcquired %d total samples.\n",totalRead);
  printf("\nEvent loop completed.\n");

  fclose(fp); // close the file
  printf("The file has been closed\n");

  return 0;
}
