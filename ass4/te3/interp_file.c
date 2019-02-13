#include "interp_file.h"

//global variables for convenience
char message[100], compare[10];
int i, found, j, k, num_task = 0;
struct resources resrcs[10];
struct task tasks[25];
struct Tuple tuple;

struct Tuple interp_file(FILE *fp){
  tasks[num_task].t_name[0] = 0;
  resrcs[num_task].r_name[0] = 0;
  while (fgets(message, sizeof(message), fp) != NULL){

    if (message[0] == 't'){
      //check to see if the message begins with task
      strcpy(compare, "task");
      i = 0;
      found = 1;
      while (message[i] != ' ' && message[i] != '\t' && message[i] != '\n'){
	if (message[i] != compare[i]){
	  found = 0;
	  break;
	}
	i++;
      }
      if (found && num_task < 25)
	create_task();
    }

    if (message[0] == 'r'){
      //check to see if the message begins with resources
      strcpy(compare, "resources");
      i = 0;
      found = 1;
      while (message[i] != ' ' && message[i] != '\t' && message[i] != '\n'){
	if (message[i] != compare[i]){
	  found = 0;
	  break;
	}
	i++;
      }
      if (found){
        res_decipher(resrcs);
	tuple.res_no = j;
      }
    }
    memset ((char *) &message, 0, sizeof message);
  }
  tuple.res = resrcs;
  tuple.tasks = tasks;
  tuple.task_no = num_task;
  return tuple;
}


//create_task will setup the task struct tasks.
void create_task(void){

  //get the task name
  while (message[i] == ' ' || message[i] == '\t') i++;
  k = 0;
  while (message[i] != ' ' && message[i] != '\t'){
    tasks[num_task].t_name[k] = message[i];
    i++;
    k++;
  }
  tasks[num_task].t_name[k] = 0;

  //get the busy time
  while (message[i] == ' ' || message[i] == '\t') i++;
  k = 0;
  while (isdigit(message[i])){
    compare[k] = message[i];
    k++;
    i++;
  }
  compare[k] = 0;
  tasks[num_task].busyTime = atoi(compare);

  //get the idle time
  while (message[i] == ' ' || message[i] == '\t') i++;
  k = 0;
  while (isdigit(message[i])){
    compare[k] = message[i];
    k++;
    i++;
  }
  compare[k] = 0;
  tasks[num_task].idleTime = atoi(compare);

  //get all the resources setup as a pointer to a resource struct
  res_decipher(tasks[num_task].res);
  tasks[num_task].res_no = j;

  //incriment the task count, and make the last tasks name empty.
  num_task++;
}

//get all the resources setup for the struct resources *res
void res_decipher(struct resources *res){
  j = 0;
  //ensures we check over every resource on a given line
  while(message[i] != '\n'){
    if(j > 9)
      break;

    //skip blank spaces
    while (message[i] == ' ' || message[i] == '\t' || message[i] == '\n') i++;
    if (message[i] == 0) return;

    //get the resource name
    k = 0;
    while (message[i] != ':'){
      res[j].r_name[k] = message[i];
      k++;
      i++;
    }
    res[j].r_name[k] = 0;
    i++;

    //get the resource value
    k = 0;
    while (isdigit(message[i])){
      compare[k] = message[i];
      k++;
      i++;
    }
    compare[k] = 0;
    res[j].r_val = atoi(compare);

    //incriment to the next resources struct
    j++;
    if (j <= 9)
      res[j].r_name[0] = 0;
  }
  return;
}
