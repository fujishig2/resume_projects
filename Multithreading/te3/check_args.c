#include "check_args.h"

//print out a nice error message when the args inputted are wrong.
void error_print(void){
  printf("Invalid format. Please use the following format: \n./a4tasks <input file> <monitor time greater than 0> <number of iterations>\n");
}

//checks if all the args inputted are formatted correctly
//returns NULL if something isn't formatted correctly
//returns the file descriptor if everything is formatted correctly
FILE *check_args(int argc, char *argv[]){
  int mon, i;
  FILE *fp;

  if (argc != 4){
    error_print();
    return NULL;
  }

  i = 0;
  //checks if the monitor time is an integer greater than 0
  while (argv[2][i] != 0){
    if (!isdigit(argv[2][i])){
      error_print();
      return NULL;
    }
    i++;
  }
  
  //convert the monitor time to an integer
  mon = atoi(argv[2]);

  //ensure the monitor time is at least 1
  if(mon < 1){
    error_print();
    return NULL;
  }

  i = 0;
  //check to see if number of iterations is an integer greater than 0
  while (argv[3][i] != 0){
    if (!isdigit(argv[3][i])){
      error_print();
      return NULL;
    }
    i++;
  }

  //check to see if the file path inputted is a file
  fp = fopen(argv[1], "r");
  if (fp == NULL){
    printf("Error: %s\n", strerror(errno));
    return NULL;
  }
  
  return fp;
}
