#ifndef GLOBALS
#define GLOBALS

#include <string.h>
#include <stdio.h>
#include <ctype.h>
#include <stdlib.h>
#include <pthread.h> 
#include <semaphore.h>
#include <errno.h>
#include <unistd.h>
#include <signal.h>

struct resources{
  char r_name[10];
  int r_val;
};
struct task{
  char t_name[10];
  int busyTime, idleTime, res_no;
  struct resources res[10];
};
struct Tuple{
  struct resources *res;
  struct task *tasks;
  int res_no, task_no;
};
#endif
