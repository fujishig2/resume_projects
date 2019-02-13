#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/times.h>
#include <unistd.h>
#include <sys/resource.h>
#include <string.h>

//global variables
pid_t pid, pid_a[32];
struct tms tmsstart, tmsend;
clock_t start, end;
char message[100], action[100], cmd[32][100], pgm[30], arg1[20], arg2[20],arg3[20],arg4[20];
char *c;
int i, found, p, a, j;

//set the resource limit
int set_limit(int i){
   struct rlimit olimit, nlimit;
   if (getrlimit(RLIMIT_CPU, &olimit) < 0){
    printf("getrlimit error\n");
    return -1;
  }
  nlimit = olimit;
  nlimit.rlim_cur = i;
  if (setrlimit(RLIMIT_CPU, &nlimit) < 0){
    printf("setrlimit error\n");
    return -1;
  }
  return 0;
}

//tell how much time has passed between the beginning and the time this was called
struct tms tell_time(clock_t real, struct tms *tmsstart, struct tms *tmsend){
  static long clktck = 0;
  clktck = sysconf(_SC_CLK_TCK);
  printf(" real: %7.2f\n", real / (double) clktck);
  printf(" user: %7.2f\n",
	 (tmsend->tms_utime - tmsstart->tms_utime) / (double) clktck);
  printf(" sys: %7.2f\n", (tmsend->tms_stime - tmsstart->tms_stime) / (double) clktck);
  printf(" child user: %7.2f\n",(tmsend->tms_cutime - tmsstart->tms_cutime) / (double) clktck);
  printf(" child sys: %7.2f\n",
	 (tmsend->tms_cstime - tmsstart->tms_cstime) / (double) clktck);
}

//put the user command into arrays based off of how many arguments are given.
//Max # of arguments allowed is 4.
void get_message(void){
  while(message[i] != 0){
	  
    if (message[i] == ' '){
      p = 0;
      a++;
      i++;
    }
	  
    switch (a) {
    case 0:
      pgm[p] = message[i];
      p++;
      pgm[p] = 0;
      break;
    case 1:
      arg1[p] = message[i];
      p++;
      arg1[p] = 0;
      break;
    case 2:
      arg2[p] = message[i];
      p++;
      arg2[p] = 0;
      break;
    case 3:
      arg3[p] = message[i];
      p++;
      arg3[p] = 0;
      break;
    case 4:
      arg4[p] = message[i];
      p++;
      arg4[p] = 0;
      break;
    default:
      found = 0;
      break;
    }
    if (found == 0){
      printf("Error! Too many arguments inputted\n");
      break;
    }
    i++;
  }
  return;
}

//runs the child. Up to 4 arguments can be given to execlp.
void run_child(void){
  switch(a){
  case 0:
    execlp(pgm, pgm, (char *) NULL);
    for(i = strlen(pgm); i >= 0; i--)
      pgm[i+2] = pgm[i];
    pgm[0] = '.';
    pgm[1] = '/';
    execlp(pgm, pgm, (char *) NULL);
    kill(getpid(), SIGKILL);
    break;
  case 1:
    execlp(pgm, pgm, arg1, (char *) NULL);
    for(i = strlen(pgm); i >= 0; i--)
      pgm[i+2] = pgm[i];
    pgm[0] = '.';
    pgm[1] = '/';
    execlp(pgm, pgm, arg1, arg2, arg3, arg4, (char*) NULL);
    kill(getpid(), SIGKILL);
    break;
  case 2:
    execlp(pgm, pgm, arg1, arg2, (char *) NULL);
    for(i = strlen(pgm); i >= 0; i--)
      pgm[i+2] = pgm[i];
    pgm[0] = '.';
    pgm[1] = '/';
    execlp(pgm, pgm, arg1, arg2, arg3, arg4, (char*) NULL);
    kill(getpid(), SIGKILL);
    break;
  case 3:
    execlp(pgm, pgm, arg1, arg2, arg3, (char *) NULL);
    for(i = strlen(pgm); i >= 0; i--)
      pgm[i+2] = pgm[i];
    pgm[0] = '.';
    pgm[1] = '/';
    execlp(pgm, pgm, arg1, arg2, arg3, arg4, (char*) NULL);
    kill(getpid(), SIGKILL);
    break;
  case 4:
    execlp(pgm, pgm, arg1, arg2, arg3, arg4, (char*) NULL);
    for(i = strlen(pgm); i >= 0; i--)
      pgm[i+2] = pgm[i];
    pgm[0] = '.';
    pgm[1] = '/';
    execlp(pgm, pgm, arg1, arg2, arg3, arg4, (char*) NULL);
    kill(getpid(), SIGKILL);
    break;  
  }
}

//save the command into the array cmd
void save_cmd(void){
  for (i=4; i < strlen(message); i++) {
    cmd[j][a] = message[i];
    a++;
  }
  cmd[j][a] = 0;
  j++;
}


void print_list(void){
  for (i = 0; i < j; i++){
    printf("%d:  (pid=\t%d,  cmd = %s)\n",i, pid_a[i], cmd[i]);
  }
}
  

int main(void){

  //set resource limit to 300
  if (set_limit(300) < 0) return 0;

  //get the start time
  if ((start = times(&tmsstart)) < 0){
    printf("times error\n");
    return 0;
  }

  pid = getpid();
  for(;;) {
    printf("a1jobs[%d]: ", pid);

    //get user prompt
    c = message;
    while((*c = getchar()) != '\n') c++;
    *c = 0;

    //list
    strcpy(action, "list");
    found = 0;
    for (i=0; message[i] == action[i]; i++) {
      if (action[i] == 0) {
        found = 1;
	break;
      }
    }
    if (found){
      print_list();
    }

    //run
    strcpy(action, "run ");
    found = 0;
    for (i=0; message[i] == action[i]; i++) {
      if (strlen(action) == i+1) {
        found = 1;
      }
    }
    i--;
    if (found){

      //process the message after "run "
      if (message[i] == ' '){
	i++;
	p = 0;
	a = 0;
	get_message();

	if (found){
	  i = 0;
	  //fork and use the child process to run the command
	  pid_a[j] = fork();
	  if (pid_a[j] == 0)
	    run_child();
	}
      }
      //if there isn't a space after run, we don't count this.
      else
	found = 0;
      
      if (found) {
	a = 0;
	if (j < 32)
	  save_cmd();
      }	  
    }

    
    

    //suspend
    strcpy(action, "suspend ");
    found = 0;
    for (i=0; message[i] == action[i]; i++) {
      if (strlen(action) == i+1){
        found = 1;
      }
    }
    i--;
    if (found){
      i++;
      a = 0;
      while (message[i] != 0){
	arg1[a] = message[i];
	i++;
	a++;
      }
      arg1[a] = 0;
      found = atoi(arg1);
      kill(found, SIGSTOP); 
    }

    //resume
    strcpy(action, "resume ");
    found = 0;
    for (i=0; message[i] == action[i]; i++) {
      if (strlen(action) == i+1){
        found = 1;
      }
    }
    i--;
    if (found){
      i++;
      a = 0;
      while (message[i] != 0){
	arg1[a] = message[i];
	i++;
	a++;
      }
      arg1[a] = 0;
      found = atoi(arg1);
      kill(found, SIGCONT); 
    }

    //terminate
    strcpy(action, "terminate ");
    found = 0;
    for (i=0; message[i] == action[i]; i++) {
      if (strlen(action) == i+1){
        found = 1;
      }
    }
    i--;
    if (found){
      i++;
      a = 0;
      while (message[i] != 0){
	arg1[a] = message[i];
	i++;
	a++;
      }
      arg1[a] = 0;
      found = atoi(arg1);
      kill(found, SIGKILL); 
    }

    //exit
    strcpy(action, "exit");
    found = 0;
    for (i=0; message[i] == action[i]; i++) {
      if (action[i] == 0) {
        found = 1;
	break;
      }
    }
    if (found){
      for (i = 0; i < j; i++){
	printf("\tjob %d terminated\n", pid_a[i]);
	kill(pid_a[i], SIGKILL);
      }
      
      if ((end = times(&tmsend)) < 0){
	printf("times error");
	return 0;
      }
      printf("\n\n");
      tell_time(end-start, &tmsstart, &tmsend);
      return 0;
    }

    //quit
    strcpy(action, "quit");
    found = 0;
    for (i=0; message[i] == action[i]; i++) {
      if (action[i] == 0) {
        found = 1;
	break;
      }
    }
    if (found){
      
      if ((end = times(&tmsend)) < 0){
	printf("times error");
	return 0;
      }
      printf("\n\n");
      tell_time(end-start, &tmsstart, &tmsend);
      return 0;
    }

    
  }
}
