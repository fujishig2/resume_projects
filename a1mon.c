#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/times.h>
#include <unistd.h>
#include <sys/resource.h>
#include <string.h>

//global variables
FILE *fp;
char s[1000], cpid[20], ppid[20], cmd[1000][1000], cmd_end[1000][1000];
int i = 1, counter, k, l, m, n, found, inside, p, z;
pid_t p_pid[1000], pid[1000], target_pid, currpid, pid_end[1000], children[100];
struct tms tmsstart, tmsend;
clock_t start, end;

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

//print the header
void print_header(char *pgm, long counter, pid_t currpid, pid_t target_pid, int interval){
  printf("\n\n\n\n%s [counter= %lu, pid = %d, target_pid= %d, interval = %d sec): \n", pgm, counter, currpid, target_pid, interval);
}


//recursive function to locate all subtrees
void locate_trees(pid_t temp_pid){
  //check all parent pids to see if they are children of the
  //temp pid
  for(l = 0; l < n; l++){
    if (temp_pid == p_pid[l]){
      m = 0;

      //check to see if the pid is already recorded in pid_end
      for(k = 0; k < z; k++){
	if (pid_end[k] == pid[l]){
	  m = 1;
	  break;
	}
      }

      //if it isn't recorded, we add it to pid_end,
      //copy down the command, and recurse.
      if (!m){
	pid_end[z] = pid[l];
	strcpy(cmd_end[z], cmd[l]);
	z++;
	locate_trees(pid_end[z-1]);
      }
    }
  }
  return;
}

int main(int argc, char *argv[]){
  //set resource limit to 300
  if (set_limit(300) < 0) return 0;
  //if there is a target pid and interval set, we run this program
  if (argc == 3){
    //save current time
    start = times(&tmsstart);
    currpid = getpid();
    static long clktck = 0;
    clktck = sysconf(_SC_CLK_TCK);
    target_pid = atoi(argv[1]);
    counter = atoi(argv[2]);
    i = 0;
    n = 0;
    inside = 0;
    p = 0;
    z = 0;

    //setup the infinite loop
    for (;;){
      found = 0;
      end = times(&tmsend);
      
      print_header(argv[0], ((end-start)/clktck), currpid, target_pid, counter);
      
      fp = popen("ps -u $USER -o user,pid,ppid,state,start,cmd --sort start", "r");
      n = 0;

      //read all lines given from ps command
      while(fgets(s, 1000, fp) != NULL){
	printf("%s", s);
	k = 0;
	l = 0;
	m = 0;
	p = 0;
	i = 0;
	while(s[i] != '\n'){

	  //skip over all blank spaces, and note
	  //when we found them by using k
	  if (s[i] == ' '){
	    k++;
	    while (s[i] == ' ')
	      i++;
	    i--;
	  }
	  
	  //gets the pid#
	  else if(k == 1){
	    cpid[l] = s[i];
	    l++;
	    cpid[l] = 0;
	  }

	  //gets the ppid#
	  else if(k == 2){
	    ppid[m] = s[i];
	    m++;
	    ppid[m] = 0;
	  }

	  //gets the command
	  else if(k == 5){
	    cmd[n][p] = s[i];
	    p++;
	    cmd[n][p] = 0;
	  }
	  i++;
	      
	}

	//get pids converted to integers
	pid[n] = atoi(cpid);
	p_pid[n] = atoi(ppid);

	//if we find the target_pid, we know it's still running.
	if (pid[n] == target_pid)
	  found = 1;

	//find all processes who are children of the target pid
	//children array holds all children of the target pid
	//pid_end holds all connected arrays.
	if (p_pid[n] == target_pid){
	  p = 0;

	  //checks to see if pid were looking at is in children
	  for (m = 0; m < inside; m++){
	    if (children[m] == pid[n])
	      p = 1;
	  }
	  if (!p){
	    //adds pid to childen
	    children[inside] = pid[n];
	    p= 0;

	    //checks to see if pid is in pid_end
	    for (l = 0; l < z; l++){
	      if (pid_end[l] == children[inside]){
		p = 1;
		break;
	      }
	    }
	    if (!p){
	      //copies the message and pid if pid isnt in pid_end
	      pid_end[z] = children[inside];
	      strcpy(cmd_end[z], cmd[n]);
	      inside++;
	      z++;
	    }
	  }
	}
	n++;
      }

      //finished reading over all the lines past this point:
      pclose(fp);

      //checks to see if there are any pids in the monitored processes from
      //before who are no longer active now. If they aren't, we update
      //pid end and the commands for them.
      for (k = z; k >= 0; k--){
	l = 0;
	for (i = 0; i < n; i++)
	  if (pid_end[k] == pid[i])
	    l = 1;
	if (!l){
	  pid_end[k] = 0;
	  cmd_end[k][0] = 0;
	  for (m = k; m < z-1; m++){
	    pid_end[m] = pid_end[m+1];
	    strcpy(cmd_end[m], cmd_end[m+1]);
	  }
	  z--;
	}
      }
	
	  
      //check all the subtrees
      for (i = 0; i < z; i++)
	locate_trees(pid_end[i]);

      //print the processes being monitored
      printf("\n------------------------------------------\n");
      printf("List of monitored processes: \n");
      for (i = 0; i < inside; i++)
	printf("%d: [%d, %s], ", i, children[i], cmd_end[i]);
      printf("\n------------------------------------------\n");

      //if process was killed, we terminate all
      //processes being monitored
      if (!found){
	printf("Target has terminated; cleaning up\n\n");
	i = 0;
	while(pid_end[i] != 0 && cmd_end != 0){
	  printf("terminating [%d, %s]\n", pid_end[i], cmd_end[i]);
	  kill (pid_end[i], SIGKILL);
	  i++;
	}
	printf("exiting %s\n", argv[0]);
	return 0;
      }
      sleep(counter);
    }
    
  }
  else
    printf("Incorrect usage. Input usage:\n%s <target_pid> <interval in sec>\n", argv[0]);
  
  
	   
  return 0;
}
