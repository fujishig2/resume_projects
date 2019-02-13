#include "check_args.h"
#include "interp_file.h"
#include "create_threads.h"

int main(int argc, char *argv[]){
  //error check the arguments inputted
  FILE *fp = check_args(argc, argv);
  if(fp == NULL)
    return -1;

  //get the resources and tasks setup as structs, and
  //place them within a tuple
  struct Tuple tuple;
  tuple = interp_file(fp);
  
  create_threads(tuple, atoi(argv[2]), atoi(argv[3]));
  
  return 0;
}
