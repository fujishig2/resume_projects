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





/*int i, j;
  printf("resources: ");
  printf("%d\n", tuple.res_no);
  for (i=0; i < tuple.res_no; i++){
    printf(" %s:%d ", tuple.res[i].r_name, tuple.res[i].r_val);
  }
  printf("\ntasks: ");
  for (i=0; i < tuple.task_no; i++){
    printf("\n%s  %d  %d ", tuple.tasks[i].t_name, tuple.tasks[i].busyTime, tuple.tasks[i].idleTime);
    j = 0;
    while (tuple.tasks[i].res[j].r_name[0] != 0 && j < 10){
      printf(" %s:%d ", tuple.tasks[i].res[j].r_name, tuple.tasks[i].res[j].r_val);
      j++;
    }
  }*/
