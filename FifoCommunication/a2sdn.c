#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <sys/times.h>
#include <unistd.h>
#include <sys/resource.h>
#include <string.h>
#include <ctype.h>
#include <sys/stat.h>
#include <poll.h>
#include <fcntl.h>
#include <errno.h>

#define MAX_NSW 7
#define MAXIP 1000
int IPLOW, IPHIGH;

struct swi{
  int port1;
  int port2;
  char port3[20];
};

struct flow{
  int destIPHigh;
  int destIPLow;
  char action[10];
  int act;
  int pri;
  int pktCount;
};
  


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

//print an error message
void improper_usage(void){
  printf("Error! Improper usage of function. Enter either: \n\"./a2sdn cont <number of switches, must be less than or equal to 7>\" for controller or \n\"./a2sdn swi trafficFile [null|swj] [null|swk] IPlow-IPhigh\" for switch\n");
}

//check if the input for the switch is correct
FILE *error_check_switch(int argc, char *argv[]){
  int i, j, k;
  char s[12], p[12];
  FILE *fp;
  strcpy(s, "sw");
  i = 0;
  if (argc != 6){
    improper_usage();
    return NULL;
  }
  
  while (argv[1][i] != 0){
      
    i++;
    if (argv[1][i] != s[i] && i < 2){
      improper_usage();
      return NULL;
    }

    if (!isdigit(argv[1][i]) && i == 2){
      improper_usage();
      return NULL;
    }

    j = argv[1][i] - '0';
    if (i == 2 && (j > 7 || j < 1)){
      improper_usage();
      return NULL;
    }

    if (argv[1][i] != 0 && i > 2){
      improper_usage();
      return NULL;
    }     
  }
  fp = fopen(argv[2], "r");
  if (fp == NULL){
    printf("Error: %s\n",strerror(errno));
    return NULL;
  }

  j = 1;
  if(!isdigit(argv[3][2]))
    j = 0;

  i=0;
  
  if (j == 0){
    strcpy(s, "null");
    for(i=0; i<5; i++){
      if (argv[3][i] != s[i]){
	improper_usage();
	return NULL;
      }
      i++;
    }
  }
  else{
    strcpy(s, "sw");
    if (argv[3][3] != 0){
      improper_usage();
      return NULL;
    }
    if (argv[3][0] != 's'){
      improper_usage();
      return NULL;
    }
    if (argv[3][1] != 'w'){
      improper_usage();
      return NULL;
    }
    j = argv[3][2]-'0';
    if (j < 1 || j > MAX_NSW){
      improper_usage();
      return NULL;
    }
  }

  j = 1;
  if(!isdigit(argv[4][2]))
    j = 0;

  i=0;
  
  if (j == 0){
    strcpy(s, "null");
    for(i=0; i<5; i++){
      if (argv[4][i] != s[i]){
	improper_usage();
	return NULL;
      }
      i++;
    }
  }
  else{
    strcpy(s, "sw");
    if (argv[4][3] != 0){
      improper_usage();
      return NULL;
    }
    if (argv[4][0] != 's'){
      improper_usage();
      return NULL;
    }
    if (argv[4][1] != 'w'){
      improper_usage();
      return NULL;
    }
    j = argv[4][2]-'0';
    if (j < 1 || j > MAX_NSW){
      improper_usage();
      return NULL;
    }
  }

  i = 0;
  while(argv[5][i] != '-' && argv[5][i] != 0){
    if(!isdigit(argv[5][i])){
      improper_usage();
      return NULL;
    }
    s[i] = argv[5][i];
    i++;
  }
  if (argv[5][i] == 0){
    improper_usage();
    return NULL;
  }
  s[i] = 0;
  i++;
  IPLOW = atoi(s);
  k=0;
  s[k] = 0;
  if (IPLOW < 0 || IPLOW > 1000){
    improper_usage();
    return NULL;
  }
    
  while(argv[5][i] != 0){
    if(!isdigit(argv[5][i])){
      improper_usage();
      return NULL;
    }
    s[k] = argv[5][i];
    i++;
    k++;
  }
  s[k] = 0;

  IPHIGH = atoi(s);
  if (IPHIGH < 0 || IPHIGH > 1000 || IPHIGH < IPLOW){
    improper_usage();
    return NULL;
  }
  return fp;
}

//check if the input for controller is correct
int error_check_cont(int argc, char *argv[]){
  char cont[5];
  int i;
  strcpy(cont, "cont");
  
  if (argc != 3){
    improper_usage();
    return -1;
  }
  i = 0;
  while (cont[i] != 0){
    i++;
    if (argv[1][i] != cont[i]){
      improper_usage();
      return -1;
    }
  }

  i=0;
    
  while (argv[2][i] != 0){
    if (!isdigit(argv[2][i]) || i > 0){
      improper_usage();
      return -1;
    }
    i++;
  }

  i = atoi(argv[2]);
  if (i > MAX_NSW || i < 1){
    improper_usage();
    return -1;
  }
  return i;
}














void swich(int argc, char *argv[], FILE *fp){
  char packet[1000], s[100], c[100], source[20], message[100], fifo[10]="fifo-0-0", ent[100];
  int fd, i, found, j, k, src, dest, opn=0, qry=0, ack=0, adm=0, addr=0, rlyin=0, rlyout=0, p, count, pktCount = 0, curr=0, flo;
  struct pollfd in_sw[9];
  struct flow flows[100];
  fifo[5]=argv[1][2];
  for (i = 0; i < 100; i++){
    flows[i].pktCount = 0;
  }
  flo = 0;
    

  //send an open packet to the controller
  fd = open(fifo, O_WRONLY);
  strcpy(packet, "[OPEN]:\n\tport0= cont, port1= ");
  strcat(packet, argv[3]);
  strcat(packet, ", port2= ");
  strcat(packet, argv[4]);
  strcat(packet, ", port3= ");
  strcat(packet, argv[5]);
  write(fd, packet, strlen(packet)+1);
  printf("Transmitted (src= %s, dest= cont) %s\n", argv[1], packet);
  opn++;

  
  while(1){

    for (i=0; i<8; i++){
      fifo[5] = i + '0';
      fifo[7] = argv[1][2];
      in_sw[i].fd = open(fifo, O_RDONLY | O_NONBLOCK);
      in_sw[i].events = POLL_IN;
    }
    

    in_sw[8].fd = STDIN_FILENO;
    in_sw[8].events = POLL_IN;

    //setup the poll to poll for user input or read from a file.
    i = poll(in_sw, 9, -1);


    //fifo reading section
    for (i=0; i < 8; i++){
      if (in_sw[i].revents & POLLIN){
	//read the fifo
        if (read(in_sw[i].fd, &packet, sizeof(char)*1000) < 0){
	  printf("error: %s", strerror(errno));
	}

	//setup source
	if (i == 0)
	  strcpy(source,"cont");
	else{
	  strcpy(source, "sw0");
	  source[2] = source[2] + i;
	}
	//print the message we've received
	printf("Received (src= %s, dest= %s) %s\n", source, argv[1], packet);

	
	//check to see if this is an acknowledge message
	strcpy(ent, "[ACK]");
	found = 1;
	j = 0;
	while (ent[j] != 0){
	  if (ent[j] != packet[j])
	    found = 0;
	  j++;
	}
	if(found)
	  ack++;




	
	//check to see if this is an add message
	strcpy(ent, "[ADD]");
	found = 1;
	j = 0;
	while (ent[j] != 0){
	  if (ent[j] != packet[j])
	    found = 0;
	  j++;
	}

	//process the add message
	if(found){
	  addr++;
	  while(packet[j] != 'a') j++;
	  while(!isdigit(packet[j])) j++;

	  //get the switch we either forward to, or 0 if it's drop.
	  p = packet[j] - '0';
	  
	  //get the low range of IP addresses for swp
	  j = 0;
	  while (packet[j] != 'd') j++;
	  while (!isdigit(packet[j])) j++;
	  k = 0;
	  while(isdigit(packet[j])){
	    s[k]=packet[j];
	    k++;
	    j++;
	  }
	    
	  s[k] = 0;
	  flows[flo].destIPLow = atoi(s);
	    
	  //get the high range of IP addresses for swp
	  while(!isdigit(packet[j]))j++;
	  k=0;
	  while(isdigit(packet[j])){
	    s[k]=packet[j];
	    k++;
	    j++;
	  }
	  s[k]=0;
	  flows[flo].destIPHigh = atoi(s);
	  flows[flo].pktCount++;

	  
	  //if it's greater than 0, we know that we are dealing with a forward
	  //thus, we will be relaying the message out.
	  if (p > 0){
	    adm++;
	    //get the source IP and destination IP from the message
	    //that called the query that got to this point.
	    k=0;
	    j=3;
	    while(!isdigit(message[j])) j++;
	    while(isdigit(message[j])){
	      s[k] = message[j];
	      k++;
	      j++;
	    }
	    s[k] = 0;
	    k=0;
	    while(!isdigit(message[j])) j++;
	    while(isdigit(message[j])){
	      c[k] = message[j];
	      k++;
	      j++;
	    }
	    c[k]=0;

	    //relay the packet towards the switch that takes care of it.
	    fifo[5]=argv[1][2];
	    if('0'+p > argv[1][2]){
	      fifo[7]=argv[1][2]+1;
	      flows[flo].act = 2;
	    }
	    
	    else{
	      fifo[7]=argv[1][2]-1;
	      flows[flo].act = 1;
	    }
	    strcpy(flows[flo].action, "FORWARD:");
	    fd = open(fifo, O_WRONLY);
	    strcpy(ent, "[RELAY]:\theader= (srcIP= ");
	    strcat(ent, s);
	    strcat(ent, ", destIP= ");
	    strcat(ent, c);
	    strcat(ent, ")");
	    write(fd, ent, strlen(packet)+1);
	    printf("Transmitted (src= %s, dest= cont) %s\n", argv[1], ent);
	    rlyout++;
	    flo++;
	  }

	  //if this a drop command, we simply go into the drop list
	  //and depending on what IP is being dropped, that will
	  //make the drop[IP] = # of packets dropped.
	  else{
	    strcpy(flows[flo].action, "DROP:");
	    flows[flo].act = 0;
	    flo++;
	  }
	  
	}

	

	//check to see if polling the fifo is a relay message
	strcpy(ent, "[RELAY]");
	found = 1;
	j = 0;
	while (ent[j] != 0){
	  if (ent[j] != packet[j])
	    found = 0;
	  j++;
	}

	//we've been relayed a message by a switch.
	if(found){
	  adm++;
	  rlyin++;
	  while(!isdigit(packet[j])) j++;
	  while(isdigit(packet[j])) j++;
	  while(!isdigit(packet[j])) j++;

	  //interpret the destination IP
	  k = 0;
	  while(isdigit(packet[j])){
	    s[k] = packet[j];
	    j++;
	    k++;
	  }
	  s[k] = 0;
	  j = atoi(s);
	  found = 0;
	  if (j>= IPLOW && j <= IPHIGH)
	    pktCount++;
	  
	  //if it isn't within our range, we have to relay it out.
	  //this part finds the swi which we are relaying to.
	  else{
	  
	    for (k = 0; k < flo; k++){
	      if(j >= flows[k].destIPLow && j <= flows[k].destIPHigh){
		found = k;
		break;
	      }
	    }
	    flows[found].pktCount++;

	    //write to the fifo that we are relaying to.
	    fifo[5]=argv[1][2];
	    if ('0'+found+1 > argv[1][2])
	      fifo[7]=argv[1][2]+1;
	    else
	      fifo[7]=argv[1][2]-1;
	    fd = open(fifo, O_WRONLY);
	    write(fd, packet, strlen(packet)+1);
	    printf("Transmitted (src= %s, dest= cont) %s\n", argv[1], packet);
	    rlyout++;
	  }
	}

	
	  






	
        //read the traffic file
	while(1){
	  if(fgets(message, sizeof(message), fp) != NULL){
	    //check for comments and spaces
	    if(message[0] != '#' && message[0] != ' '){

	      //get the source IP address from traffic file
	      j = 3;
	      while (!isdigit(message[j])) j++;
	      k=0;
	      while (isdigit(message[j])){
		s[k] = message[j];
		j++;
		k++;
	      }
	      s[k]=0;
		

	      //get the dest IP address from the traffic file
	      while (!isdigit(message[j])) j++;
	      k=0;
	      while (isdigit(message[j])){
		c[k] = message[j];
		j++;
		k++;
	      }
	      c[k]=0;

	      //make the source and destination IP's integers.
	      src = atoi(s);
	      dest = atoi(c);

	      //check to see if this is for the current switch
	      if (message[2] == argv[1][2]){
		//check to see if the source IP is within the current range
		if (src <= IPHIGH && src >= IPLOW){
		  found = 0;
		  //check to see if destination IP is within the range of
		  //other known switches.
		  for (j = 0; j < flo; j++){
		    if (dest <= flows[j].destIPHigh && dest >= flows[j].destIPLow){
		      fifo[5]=argv[1][2];
		      if ('0'+j+1 > argv[1][2])
			fifo[7]=argv[1][2]+1;
		      else
			fifo[7]=argv[1][2]-1;
		      
		      flows[j].pktCount++;
		      fd = open(fifo, O_WRONLY);
		      strcpy(packet, "[RELAY]:\theader= (srcIP= ");
		      strcat(packet, s);
		      strcat(packet, ", destIP= ");
		      strcat(packet, c);
		      strcat(packet, ")");
		      write(fd, packet, strlen(packet)+1);
		      printf("Transmitted (src= %s, dest= cont) %s\n", argv[1], packet);
		      rlyout++;
		      adm++;
		      found = 1;
		    }
		  }
		  //if the destination IP is within the current switches
		  //range, we simply admit it.
		  if(dest <= IPHIGH && dest >= IPLOW){
		    adm++;
		    pktCount++;
		    found = 1;
		  }
		  
		  //if we can't find the range for the destination IP
		  //we must query the controller
		  if(found != 1) {
		    //query controller
		    fifo[5]=argv[1][2];
		    fifo[7]='0';
		    fd = open(fifo, O_WRONLY);
		    strcpy(packet, "[QUERY]:\theader= (srcIP= ");
		    strcat(packet, s);
		    strcat(packet, ", destIP= ");
		    strcat(packet, c);
		    strcat(packet, ")");
		    write(fd, packet, strlen(packet)+1);
		    printf("Transmitted (src= %s, dest= cont) %s\n", argv[1], packet);
		    qry++;
		    break;
		  }
		}
	      }
	    }
	  }

	    
	  else {
	    break;
	  }
	}
      }
    }



    //user input section
    if (in_sw[8].revents & POLLIN){
      read(0, s, 99);

      //check if this is an exit command
      strcpy(c, "exit\n");
      found = 1;
      for (i=0; i<5; i++){
	if (s[i] != c[i]){
	  found = 0;
	  break;
	}
      }
      if (found){
	printf("Exitting.\n");
	return;
      }

      //check to see if this is a list command.
      strcpy(c, "list\n");
      found = 1;
      for (i=0; i<5; i++){
	if (s[i] != c[i]){
	  found = 0;
	  break;
	}
      }

      //print the flow table
      if (found){
	printf("Flow table:\n");

	//print the current flow
	strcpy(s, "[");
	sprintf(c, "%d", 0);
	strcat(s, c);
	strcat(s, "]\t(srcIP= 0-1000, destIP= ");
	sprintf(c, "%d", IPLOW);
	strcat(s, c);
	strcat(s, "-");
	sprintf(c, "%d", IPHIGH);
	strcat(s, c);
	strcat(s,", action= FORWARD:");
	j = 3;
	sprintf(c, "%d", j);
	strcat(s, c);
	strcat(s, ", pri= 4, pktCount= ");
	sprintf(c, "%d", pktCount);
	strcat(s, c);
	strcat(s, ")");
	printf("%s\n", s);
	//print all the flows that were admitted
	for (i=0; i<flo; i++)
	  {
	    strcpy(s, "[");
	    sprintf(c, "%d", i+1);
	    strcat(s, c);
	    strcat(s, "]\t(srcIP= 0-1000, destIP= ");
	    sprintf(c, "%d", flows[i].destIPLow);
	    strcat(s, c);
	    strcat(s, "-");
	    sprintf(c, "%d", flows[i].destIPHigh);
	    strcat(s, c);
	    strcat(s,", action= ");
	    strcat(s, flows[i].action);
	    sprintf(c, "%d", flows[i].act);
	    strcat(s, c);
	    strcat(s, ", pri= 4, pktCount= ");
	    sprintf(c, "%d", flows[i].pktCount);
	    strcat(s, c);
	    strcat(s, ")");
	    printf("%s\n", s);
	  }
	

	
	
	printf("\nPacket Stats:\n");
	printf("\tReceived:\tADMIT: %d,\tACK: %d,\tADDRULE:%d,\tRELAYIN:%d\n",adm, ack, addr, rlyin);
	printf("\tTransmitted:\tOPEN: %d,\tQUERY: %d,\tRELAYOUT: %d\n", opn, qry, rlyout);
      }

      else printf("Invalid command.\n");
    }
  }
}


void controller(int sw, int argc, char *argv[]){
  
  char c[6], s[100], sw2cont[1000], fifo[15] = "fifo-0-0", message[100], arr[10], desti[6];
  int i, ret_poll, fd, found, admitted[7] = {0,0,0,0,0,0,0}, j, k, l, opn=0, qry=0, ack=0, add=0, src, dest, action=0;
  struct swi Switches[7];
  struct pollfd input[sw+1];
  while(1){

    //setup the poll to poll in the stdin, as well as the fifo's
    input[0].fd = STDIN_FILENO;
    input[0].events = POLL_IN;
    for (i=1; i<sw+1; i++){
      fifo[5] = i + '0';
      fifo[7] = '0';
      s[8] = 0;
      input[i].fd = open(fifo, O_RDONLY | O_NONBLOCK);
      input[i].events = POLL_IN;
    }
    ret_poll = poll(input, sw+1, -1);

    //get user input from the poll
    if (input[0].revents & POLLIN){

      //check if user input an exit command
      read(0, s, 99);
      strcpy(c, "exit\n");
      found = 1;
      for (i=0; i<5; i++){
	if (s[i] != c[i]){
	  found = 0;
	  break;
	}
      }
      if (found){
	printf("Exitting.\n");
	return;
      }

      //check if the user input a list command  
      strcpy(c, "list\n");
      found = 1;
      for (i=0; i<5; i++){
	if (s[i] != c[i]){
	  found = 0;
	  break;
	}
      }
      if (found){
	//print the switch info and packet stats
	j = 0;
	for (i=0; i<7; i++)
	  j = j+admitted[i];
	printf("Switch information (nSwitch= %d):\n", j);
	for (i=0; i<7; i++){
	  if (admitted[i])
	    printf("[sw%d] port1= %d, port2= %d, port3= %s\n", i+1, Switches[i].port1, Switches[i].port2, Switches[i].port3);
	}
	printf("\nPacket Stats:\n");
	printf("Received:\tOPEN:%d,\tQUERY:%d\n",opn,qry);
	printf("Transmitted:\tACK:%d,\tADD:%d\n",ack,add);
      }

      else printf("Invalid command.\n");
    }

    
    //get input from FIFO's
    for (i=1; i < sw+1; i++){
      if (input[i].revents & POLLIN){

	//read input from fifo
	if (read(input[i].fd, &sw2cont, sizeof(char)*1000) < 0){
	  printf("error: %s", strerror(errno));
	}

	printf("Received (src= sw%d, dest= cont) %s\n", i, sw2cont);

	//check to see if this is an open packet
	strcpy(s, "[OPEN]");
	j = 0;
	found = 1;

	
	while (s[j]!= 0){
	  if (sw2cont[j] != s[j])
	    found = 0;
	  j++;
	}
	if(found) opn+=1;

	//if found and the switch hasn't been admitted, we acknowledge it.
	if(found && !admitted[i-1]){
	  admitted[i-1] =1;

	  //interpret open command, and add this switch to the
	  //struct swi switches[i-1]

	  //get port1
	  while (sw2cont[j] != '1')
	    j++;
	  j = j+5;
	  if (!isdigit(sw2cont[j]))
	    Switches[i-1].port1 = -1;
	  else
	    Switches[i-1].port1 = sw2cont[j] - '0';

	  //get port2
	  while (sw2cont[j] != '2')
	    j++;
	  j = j+5;
	  if (!isdigit(sw2cont[j]))
	    Switches[i-1].port2 = -1;
	  else
	    Switches[i-1].port2 = sw2cont[j] - '0';

	  //get port3
	  while (sw2cont[j] != '3')
	    j++;
	  j = j+3;
	  Switches[i-1].port3[0] = sw2cont[j];
	  k=0;
	  while(sw2cont[j] != 0){
	    j++;
	    k++;
	    Switches[i-1].port3[k] = sw2cont[j];
	  }


	  //transmit the ack message back to the switch who called open
	  fifo[5]='0';
	  fifo[7]=i+'0';
	  fd = open(fifo, O_WRONLY || O_NONBLOCK);
	  strcpy(s, "[ACK]");
	  write(fd, s, strlen(s)+1);
	  close(fd);
	  printf("Transmitted (src = cont, dest = sw%d) %s\n", i, s);
	  ack++;
	}

	//check to see if the message is a query message
	strcpy(s, "[QUERY]");
	j = 0;
	found = 1;
	
	while (s[j]!= 0){
	  if (sw2cont[j] != s[j])
	    found = 0;
	  j++;
	}

	
	if (found){
	  qry++;
	  j = 0;
	  
	  //get the source IP
	  while(!isdigit(sw2cont[j])) j++;
	  k=0;
	  while(isdigit(sw2cont[j])){
	    s[k] = sw2cont[j];
	    j++;
	    k++;
	  }
	  s[k] = 0;

	  //get the destination IP
	  while(!isdigit(sw2cont[j])) j++;
	  k=0;
	  while(isdigit(sw2cont[j])){
	    desti[k] = sw2cont[j];
	    j++;
	    k++;
	  }
	  desti[k] = 0;

	  //get the source and destination IPs to be integers.
	  src = atoi(s);
	  dest = atoi(desti);

	  //check to see if the destination IP is within the range
	  //of any of the admitted switches. If it is, we make
	  //action equal to the switch number.
	  action = 0;
	  for (j=0; j<7; j++){
	    if (admitted[j]){
	      k = 0;
	      while(isdigit(Switches[j].port3[k])){
		s[k] = Switches[j].port3[k];
		k++;
	      }
	      k++;
	      l=0;
	      while(isdigit(Switches[j].port3[k])){
		c[l] = Switches[j].port3[k];
		l++;
		k++;
	      }

	      IPLOW = atoi(s);
	      IPHIGH = atoi(c);

	      if(dest <= IPHIGH && dest >= IPLOW){
		action = j+1;
		break;
	      }
	    }
	  }
	  
	  fifo[5]='0';
	  fifo[7]=i+'0';
	  arr[0] = '0' + action;
	  arr[1] = 0;

	  //send an add message back to the switch which queried.
	  strcpy(message, "[ADD]\n\t(srcIP= 0-1000, destIP= ");

	  //If there are any ports which the destination IP falls within range
	  //we simply just make the message send a forward message.
	  if(action > 0){
	    strcat(message, s);
	    strcat(message, "-");
	    strcat(message, c);
	    strcat(message, ", action= FORWARD:");
	    strcat(message, arr);
	    strcat(message, ", pri= 4, pktCount= 0)");
	  }

	  //if action is 0, there are no ports for which the destination
	  //IP falls within range, thus we tell the switch to drop the
	  //packet.
	  else{
	    strcat(message, desti);
	    strcat(message, "-");
	    strcat(message, desti);
	    strcat(message, ", action= DROP:0, pri=4, pktCount= 0)");
	  }
	    
	  //send the add message to the switch which queried.
	  fd = open(fifo, O_WRONLY || O_NONBLOCK);
	  write(fd, message, strlen(message)+1);
	  close(fd);
	  printf("Transmitted (src = cont, dest = sw%d) %s\n", i, message);
	  add++;
	}
      }
    }
	
  }
  
}

    

int main(int argc, char *argv[]){
  int cont=0, sw=0;
  //set resource limit to 300
  if (set_limit(300) < 0) return 0;

  //error check the inputs and determine wheter a2sdn has been
  //invoked as a switch or controller.
  if (argc < 3) {
    improper_usage();
    return 0;
  }
  if (argv[1][0] == 'c') cont = 1;
  if (argv[1][0] == 's') sw = 1;

  if (cont < 1 && sw < 1){
    improper_usage();
    return 0;
  }


  
  //controller
  if (cont == 1){
    sw = error_check_cont(argc, argv);
    if(sw == -1) return 0;
    controller(sw, argc, argv);
    return 0;
  }
  
  //switch
  else {
    FILE *fp = error_check_switch(argc, argv);
    if (fp == NULL) return 0;
    swich(argc, argv, fp);
    return 0;
  }

  
}
