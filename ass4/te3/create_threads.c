#include "create_threads.h"

//global variables
sem_t *mutex, *mutex_pipe;
int times[25], ITER[25], status[25], iters, finished, task_no, wait[25];
struct Tuple tup;


//locks down the semaphore between task and monitor thread.
//when task writes to this, the monitor thread must be finished
//reading, thus a semaphore is used.
void task_mutex_pipe(int stat, int task_no){
  errno = EAGAIN;
  while(errno == EAGAIN){
    errno = 0;
    //tries to use semaphore. If it is full, we sleep for 10 msec
    //and try again.
    sem_trywait(&mutex_pipe[task_no]);
    if (errno == EAGAIN){
      usleep(10000);
      times[task_no] += 10;
    }
  }
  //change the status to an integer. 0 = WAIT, 1 = RUN, 2 = IDLE
  status[task_no] = stat;
  //close the semaphore
  sem_post(&mutex_pipe[task_no]);
}


//Function for task threads to run in.
void *task_thread(void *task){
  //declare variables
  struct Tuple *tuple = ((struct Tuple *) task);
  int i, j, k, l, found, sem_i[10];

  //setup thread to be waiting at the beginning
  task_mutex_pipe(0, tuple[0].task_no);

  //sem_i is the index for the current tasks resources needed.
  for (i = 0; i < 10; i++)
    sem_i[i] = -1;
  l = 0;
  //atempt to find all the indices of resources that this task uses.
  for (i = 0; i < tuple[0].tasks[0].res_no; i++){
    for (j = 0; j < tuple[0].res_no; j++){
      k = 0;
      found = 1;
      //compare the resource names between the task resources and all resources
      while(tuple[0].res[j].r_name[k] != 0){
	if (tuple[0].tasks[0].res[i].r_name[k] != tuple[0].res[j].r_name[k]){
	  found = 0;
	  break;
	}
	k++;
      }
      //save the index of the resource as its respective semaphore index.
      if (found){
	sem_i[l] = j;
	l++;
      }
    }
  }

  //each thread gets looped ITER times
  for(ITER[tuple[0].task_no] = 0; ITER[tuple[0].task_no] < iters; ITER[tuple[0].task_no]++){

    //setup tasks status as a waiting type
    task_mutex_pipe(0, tuple[0].task_no);

    //attempt to obtain the necessary resources/semaphores needed for this thread
  try_again:
    errno = 0;
    for (i = 0; i < l; i++){
      sem_trywait(&mutex[sem_i[i]]);
      if (errno == EAGAIN){
	for (j = 0; j < i; j++)
	  sem_post(&mutex[sem_i[j]]);
	//wait 10 msec if any of the resources are full, and try again
        usleep(10000);
	times[tuple[0].task_no] += 10;
	wait[tuple[0].task_no] += 10;
	
	goto try_again;
      }
    }

    //setup tasks status as a running type
    task_mutex_pipe(1, tuple[0].task_no);

    //sleep for busyTime msec
    usleep(tuple[0].tasks[0].busyTime*1000);
    times[tuple[0].task_no] += tuple[0].tasks[0].busyTime;
    
    //release the given semaphores
    for (i = 0; i < l; i++)
      sem_post(&mutex[sem_i[i]]);
    
    //setup tasks status as idle type
    task_mutex_pipe(2, tuple[0].task_no);
    
    //sleep for idleTime msec
    usleep(tuple[0].tasks[0].idleTime*1000);
    times[tuple[0].task_no] += tuple[0].tasks[0].idleTime;
  
    printf("task: %s (tid= %lu, iter= %d, time= %d msec\n", tuple[0].tasks[0].t_name, pthread_self(), ITER[tuple[0].task_no], times[tuple[0].task_no]);
  }
  pthread_exit(NULL);
}

//function for monitor thread
void *monitor_thread(void *monTime){
  
  //local variables
  int mon_time = *((int *) monTime);
  int i;
  char wait[50], run[50], idle[50];

  //loop until all tasks are completed
  while(finished == 0){

    //wait for monitorTime msec before executing the monitor thread
    i = mon_time*1000;
    usleep(i);

    //lock all semaphores which tasks use to write their status
    for(i = 0; i < task_no; i++) {
      sem_wait(&mutex_pipe[i]);
    }

    //setup the wait, run and idle strings
    strcpy(wait, "[WAIT] ");
    strcpy(run, "[RUN] ");
    strcpy(idle, "[IDLE] ");

    //check each tasks status, and copy the thread name to their respective strings.
    for(i = 0; i < task_no; i++) {
      switch(status[i]){
      case 0:
	strcat(wait, tup.tasks[i].t_name);
	strcat(wait, " ");
	break;
      case 1:
	strcat(run, tup.tasks[i].t_name);
	strcat(run, " ");
	break;
      case 2:
	strcat(idle, tup.tasks[i].t_name);
	strcat(idle, " ");
	break;
      }
    }
    
    printf("%s\n%s\n%s\n", wait, run, idle);
    //free the task status semaphores after the monitor function has printed.
    for(i = 0; i < task_no; i++) 
      sem_post(&mutex_pipe[i]);
  }
  pthread_exit(NULL);
}

//main calls create_threads to create all the threads needed
void create_threads(struct Tuple tuple, int monTime, int iter){
  //local variables
  int i, j;
  sem_t temp[tuple.res_no], temp2[tuple.task_no];

  //setup the global variables
  mutex = temp;
  mutex_pipe = temp2;
  iters = iter;
  finished = 0;
  task_no = tuple.task_no;
  tup = tuple;

  //initialize resource semaphores to have each resource's semaphore
  //hold the same amount as the resource value given in the data file
  for(i = 0; i < tuple.res_no; i++)
    sem_init(&(mutex[i]), 0, tuple.res[i].r_val);

  //initialize status semaphore. This semaphore acts as a binary semaphore
  for(i = 0; i < task_no; i++){
    sem_init(&(mutex_pipe[i]), 0, 1);
  }

  //setup task global variables
  for (i = 0; i < tuple.task_no; i++){
    times[i] = 0;
    ITER[i] = 0;
    wait[i] = 0;
    status[i] = 0;
  }

  //create all the necessary thread id's
  pthread_t task_threads[tuple.task_no], mon_thr;

  //create task thread. The argument for task thread is a tuple of
  //the current task, as well as all of the available resources
  for (i = 0; i < tuple.task_no; i++){
    struct Tuple *cur_task = malloc(sizeof *cur_task);
    cur_task[0].res = tuple.res;
    cur_task[0].res_no = tuple.res_no;
    cur_task[0].tasks = tuple.tasks+i;
    cur_task[0].task_no = i;
    pthread_create(task_threads+i, NULL, task_thread, cur_task);
  }

  //create monitor thread. The argument used for this is the
  //monitorTime value
  pthread_create(&mon_thr, NULL, monitor_thread, &monTime);
  

  //wait for all the threads to complete, ensuring that the main
  //thread doesn't finish until all threads are finished
  for (i = 0; i < tuple.task_no; i++)
    pthread_join(task_threads[i], NULL);
  finished = 1;
  pthread_join(mon_thr, NULL);

  //free all semaphores created
  for(i = 0; i < tuple.res_no; i++)
    sem_destroy(&(mutex[i]));
  for(i = 0; i < task_no; i++)
    sem_destroy(&(mutex_pipe[i]));

  //print the termination message
  printf("\nSystem Resources:\n");
  for(i = 0; i < tuple.res_no; i++)
    printf("\t%s: (maxAvail=\t%d, held=\t0\n)", tuple.res[i].r_name,  tuple.res[i].r_val);

  printf("\nSystem Tasks:\n");
  for (i = 0; i < tuple.task_no; i++){
    printf("[%d] %s (IDLE, runTime= %d msec, idleTime = %d msec):\n", i, tuple.tasks[i].t_name, tuple.tasks[i].busyTime, tuple.tasks[i].idleTime);
    printf("\t(tid= %lu)\n", task_threads[i]);
    for(j = 0; j < tuple.tasks[i].res_no; j++){
      printf("\t%s: (needed=\t%d, held=\t0)\n", tuple.tasks[i].res[j].r_name, tuple.tasks[i].res[j].r_val);
    }
    printf("(RUN: %d times, WAIT: %d msec)\n\n", iter, wait[i]);
  }
  int total_time = 0;
  for (i = 0; i < tuple.task_no; i++)
    if (times[i] > total_time)
      total_time = times[i];
  printf("Running time= %d msec\n", total_time);
  
  return;
}


