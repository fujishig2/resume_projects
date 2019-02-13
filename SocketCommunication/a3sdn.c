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
#include <sys/socket.h>
#include <netinet/in.h>
#include <sys/ioctl.h>
#include <netdb.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/timerfd.h>
#include <sys/timerfd.h>

#define MAX_NSW 7
#define MAXIP 1000
int IPLOW, IPHIGH;
int flo = 0, pktCount = 0, opn=0, qry=0, ack=0, adm=0, rlyout=0, rlyin=0, addr=0, add=0, admitted[7] = {0,0,0,0,0,0,0};

struct swi{
  int port1;
  int port2;
  char port3[20];
} Switches[7];

struct flow{
  int swNum;
  int destIPHigh;
  int destIPLow;
  char action[10];
  int act;
  int pri;
  int pktCount;
} flows[100];
  


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
  printf("Error! Improper usage of function. Enter either: \n\"./a2sdn cont <number of switches, must be less than or equal to 7> <portNumber>\" for controller or \n\"./a2sdn swi trafficFile [null|swj] [null|swk] IPlow-IPhigh serverAddress portNumber\" for switch\n");
}

//check if the input for the switch is correct
FILE *error_check_switch(int argc, char *argv[]){
  int i, j, k;
  char s[12], p[12];
  FILE *fp;
  strcpy(s, "sw");
  i = 0;
  if (argc != 8){
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

int error_check_port(char *argv[]){
  //error check the port here:
  int i = 0;
   while (argv[7][i] != 0){
    if (!isdigit(argv[7][i])){
      improper_usage();
      return -1;
    }
    i++;
  }
  return atoi(argv[7]);
}

//check if the input for controller is correct
int *error_check_cont(int argc, char *argv[]){
  char cont[5];
  int i;
  int *swi_port = (int*) malloc(sizeof(int)*2);
  strcpy(cont, "cont");
  
  if (argc != 4){
    improper_usage();
    return NULL;
  }
  i = 0;
  while (cont[i] != 0){
    i++;
    if (argv[1][i] != cont[i]){
      improper_usage();
      return NULL;
    }
  }

  i=0;
    
  while (argv[2][i] != 0){
    if (!isdigit(argv[2][i]) || i > 0){
      improper_usage();
      return NULL;
    }
    i++;
  }

  *swi_port = atoi(argv[2]);
  
  if (*swi_port > MAX_NSW || *swi_port < 1){
    improper_usage();
    return NULL;
  }

  i=0;
    
  while (argv[3][i] != 0){
    if (!isdigit(argv[3][i])){
      improper_usage();
      return NULL;
    }
    i++;
  }
  *(swi_port+1) = atoi(argv[3]);
  
  return swi_port;
}










void sig_handler_switch(int signo){
  if (signo == SIGUSR1){
    char s[1000], c[1000];
    int i, j;
    printf("\n\nFlow table:\n");

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
    i = 0;
    //print all the flows that were admitted
    while(flows[i].pktCount != 0)
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
	i++;
      }
	

	
	
    printf("\nPacket Stats:\n");
    printf("\tReceived:\tADMIT: %d,\tACK: %d,\tADDRULE:%d,\tRELAYIN:%d\n",adm, ack, addr, rlyin);
    printf("\tTransmitted:\tOPEN: %d,\tQUERY: %d,\tRELAYOUT: %d\n\n", opn, qry, rlyout);
  }
}



void swich(int argc, char *argv[], FILE *fp){
  char packet[1000], s[100], c[100], source[20], message[100], fifo[10]="fifo-0-0", ent[100], host_addr[18];
  int fd, i, found, j, k, src, dest, p, count, curr=0, flo, sock, slp = 0;
  struct pollfd in_sw[10];
  struct sockaddr_in cont_addr, sw_addr;
  struct servent *sp;                    // service entity
  struct hostent *hp;                    // host entity
  struct itimerspec timeout;
  flo = 0;
  

  
  for (i = 0; i < 100; i++){
    flows[i].pktCount = 0;
  }

  
  
  // lookup the specified host
  hp= gethostbyname(argv[6]);
  if (hp == (struct hostent *) NULL) {
    fprintf (stderr, "%s: unknown host %s\n", argv[0], argv[1]);
    exit (1);
  }
  host_addr[1] = 0;
  i = 0;
  while (hp -> h_addr_list[i] != NULL){
    strcat(host_addr, inet_ntoa( *( struct in_addr*)( hp -> h_addr_list[i])));
    i++;
  }

  
  //setup the host address and port
  memset ((char *) &cont_addr, 0, sizeof cont_addr);
  cont_addr.sin_family= hp->h_addrtype;
  cont_addr.sin_port = htons(atoi(argv[7]));
  if(inet_pton(AF_INET, host_addr, &cont_addr.sin_addr)<=0) { 
    printf("\nInvalid address/ Address not supported \n"); 
    exit(1); 
  }

  //create the socket
  if ( (sock = socket (AF_INET, SOCK_STREAM, 0)) < 0) {
    fprintf (stderr, "%s: socket \n", argv[0]);
    exit (1);
  }
  // if the socket is unbound at the time of connect(); the system
  // automatically selects and binds a name to the socket
  if (connect (sock,  (struct sockaddr *) &cont_addr,  sizeof cont_addr) < 0) {
    fprintf (stderr, "%s: connect\n", argv[0]);
    exit (1);
  }
  

  
  //send an open packet to the controller
  sprintf(packet, "(src= %s, dest= cont) ", argv[1]);
  strcat(packet, "[OPEN]:\n\tport0= cont, port1= ");
  strcat(packet, argv[3]);
  strcat(packet, ", port2= ");
  strcat(packet, argv[4]);
  strcat(packet, ", port3= ");
  strcat(packet, argv[5]);
  send(sock, packet, strlen(packet), 0);
  printf("Transmitted %s\n", packet);
  opn++;
  signal(SIGUSR1, sig_handler_switch);

  
  while(1){
    //socket poll
    in_sw[0].fd = sock;
    in_sw[0].events = POLL_IN;
    in_sw[0].revents = 0;

    //fifo polls
    for (i=1; i<8; i++){
      fifo[5] = i + '0';
      fifo[7] = argv[1][2];
      in_sw[i].fd = open(fifo, O_RDONLY | O_NONBLOCK);
      in_sw[i].events = POLL_IN;
    }
    
    //std input poll
    in_sw[8].fd = STDIN_FILENO;
    in_sw[8].events = POLL_IN;
    

    //start the poll. We check 9 input polls if delay hasn't been invoked.
    if (slp == 0)
      i = poll(in_sw, 9, -1);
    
    else
      i = poll(in_sw, 10, -1);

    //reset the delay flag and return events so we can continue reading the traffic file.
    if (in_sw[9].revents & POLLIN){
      printf("\n** Delay period ended\n\n");
      slp = 0;
      in_sw[9].revents = 0;
    }

    //check to see if the poll is from the controller
    if (in_sw[0].revents & POLLIN){
      memset ((char *) &packet, 0, sizeof(char)*1000);

      //read the message from the controller
      if(read(in_sw[0].fd, &packet, sizeof(char)*1000) < 0){
	printf("error: %s", strerror(errno));
      }
      printf("Received %s\n", packet);
      j = 0;
      while(packet[j] != '[') j++;
      
      //check to see if this is an acknowledge message
      strcpy(ent, "[ACK]");
      found = 1;
      k = 0;
      while (ent[k] != 0){
	if (ent[k] != packet[j])
	  found = 0;
	j++;
	k++;
      }
      if(found)
	ack++;




	
      //check to see if this is an add message
      strcpy(ent, "[ADD]");
      found = 1;
      j = 0;
      k = 0;
      while(packet[j] != '[') j++;
      while (ent[k] != 0){
	if (ent[k] != packet[j])
	  found = 0;
	j++;
	k++;
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
	j++;
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
	flows[flo].swNum = p;

	  
	//if it's greater than 0, we know that we are dealing with a forward
	//thus, we will be relaying the message out.
	if (p > 0){
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

	  //relay the packet towards the switch that takes care of it through fifo's.
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
	  printf("Transmitted (src= %s, dest= sw%c) %s\n", argv[1], fifo[7], ent);
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
    }


    //fifo reading section
    for (i=1; i < 8; i++){
      if (in_sw[i].revents & POLLIN){
	//read the fifo
        if (read(in_sw[i].fd, &packet, sizeof(char)*1000) < 0){
	  printf("error: %s", strerror(errno));
	}
	strcpy(source, "sw0");
	source[2] = source[2] + i;
	
	//print the message we've received
	printf("Received (src= %s, dest= %s) %s\n", source, argv[1], packet);

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
	    fd = open(fifo, O_WRONLY | O_NONBLOCK);
	    poll(0, 0, 20);
	    write(fd, packet, strlen(packet)+1);
	    printf("Transmitted (src= %s, dest= sw%c) %s\n", argv[1], fifo[7], packet);
	    rlyout++;
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
	printf("\n\nFlow table:\n");

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
	printf("\tTransmitted:\tOPEN: %d,\tQUERY: %d,\tRELAYOUT: %d\n\n", opn, qry, rlyout);
      }

      else printf("Invalid command.\n");
    }

    //we only read the traffic file if we've had an acknowledgement from the controller
    //and if delay hasn't been invoked.
    if(!slp && ack > 0){
      //read the traffic file
      while(1){
	memset ((char *) &message, 0, sizeof message);
	if(fgets(message, sizeof(message), fp) != NULL){
	  //check for comments and spaces
	  if(message[0] != '#' && message[0] != ' '){

	    //check to see if this is for the current switch
	    if (message[2] == argv[1][2]){
	      //get the source IP address from traffic file

	      j =0;
	      while(message[j] != 'd' && message[j] != 0) j++;

	      //check to see if this is a delay message
	      if (message[j] == 'd'){
		strcpy(s, "delay");
		k = 0;
		found = 1;
		while(s[k] != 0){
		  if (s[k] != message[j])
		    found = 0;
		  k++;
		  j++;
		}
		if (found){
		  //find the interval
		  while(!isdigit(message[j])) j++;
		  k=0;
		  while (isdigit(message[j])){
		    s[k] = message[j];
		    j++;
		    k++;
		  }
		  //create a timer which can be polled.
		  in_sw[9].fd = timerfd_create(CLOCK_MONOTONIC, TFD_NONBLOCK);
		  if (in_sw[9].fd <= 0) {
		    printf("Failed to create timer\n");
		    break;
		  }
		  s[k]=0;
		  //delay flag has been set.
		  slp = 1;
		  //setup the timer values
		  timeout.it_value.tv_nsec = (atoi(s)%1000)*1000000;
		  timeout.it_value.tv_sec = atoi(s)/1000;
		  timeout.it_interval.tv_nsec = 0;
		  timeout.it_interval.tv_sec = 0;
		  //setup the poll for timer
		  fd = timerfd_settime(in_sw[9].fd, 0, &timeout, NULL);
		  in_sw[9].events = POLLIN;
		  in_sw[9].revents = 0;
		  printf("\n** Entering a delay period for %s msec\n\n", s);
		  
		  break;
		}
	      }

	      //if the line in the traffic file isn't a delay message
	      else {
		adm++;
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
		      fd = open(fifo, O_WRONLY | O_NONBLOCK);
		      strcpy(packet, "[RELAY]:\theader= (srcIP= ");
		      strcat(packet, s);
		      strcat(packet, ", destIP= ");
		      strcat(packet, c);
		      strcat(packet, ")");
		      poll(0, 0, 20);
		      write(fd, packet, strlen(packet)+1);
		      printf("Transmitted (src= %s, dest= sw%c) %s\n", argv[1], fifo[7], packet);
		      rlyout++;
		      found = 1;
		    }
		  }
		  //if the destination IP is within the current switches
		  //range, we simply admit it.
		  if(dest <= IPHIGH && dest >= IPLOW){
		    pktCount++;
		    found = 1;
		  }
		  
		  //if we can't find the range for the destination IP
		  //we must query the controller
		  if(found != 1) {
		    //query controller
		    sprintf(packet, "(src = %s, dest = cont) ", argv[1]);
		    strcat(packet, "[QUERY]:\theader= (srcIP= ");
		    strcat(packet, s);
		    strcat(packet, ", destIP= ");
		    strcat(packet, c);
		    strcat(packet, ")");
		    send(sock, packet, strlen(packet), 0);
		    printf("Transmitted %s\n",packet);
		    qry++;
		    break;
		  }
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
}


void sig_handler_cont(int signo){
  if (signo == SIGUSR1){
    int j = 0, i;
    for (i=0; i<7; i++)
      if(Switches[i].port3[0] != 0)
	j++;
    printf("\n\nSwitch information (nSwitch= %d):\n", j);
    for (i=0; i<7; i++){
      if (admitted[i])
	printf("[sw%d] port1= %d, port2= %d, port3= %s\n", i+1, Switches[i].port1, Switches[i].port2, Switches[i].port3);
    }
    printf("\nPacket Stats:\n");
    printf("Received:\tOPEN:%d,\tQUERY:%d\n",opn,qry);
    printf("Transmitted:\tACK:%d,\tADD:%d\n\n",ack,add);
  }
}

void controller(int sw, int port, int argc, char *argv[]){
  
  char c[6], s[100], sw2cont[1000], message[100], arr[10], desti[6];
  int i, ret_poll, fd, cont_fd, sw_fd[sw], found, j, k, l, src, dest, action=0, numfds, sw_len, nread, sw_in;
  struct sockaddr_in cont_addr, sw_addr;
  struct pollfd input[sw+3];
  FILE *sfpin[sw+3];

  for (i=0; i<7; i++)
    Switches[i].port3[0] = 0;
    
  // Creating controller socket file descriptor 
  if ((cont_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0){ 
    fprintf (stderr, "%s: socket \n", argv[0]);
    exit (1);
  }

  //setup controller host address and port address
  cont_addr.sin_family = AF_INET;
  cont_addr.sin_addr.s_addr = htonl(INADDR_ANY);
  cont_addr.sin_port = htons(port);

  //bind the socket as a listening socket
  if ( bind (cont_fd, (struct sockaddr *) &cont_addr, sizeof cont_addr) < 0) {
    fprintf (stderr, "%s: bind errno: %d %s\n", argv[0], errno, strerror(errno));
    exit (1);
  }

  //setup the number of incoming sockets we can listen to
  listen(cont_fd, sw);

  //setup the poll for polling the controller socket
  numfds = 2;
  input[1].fd = cont_fd;
  input[1].events = POLL_IN;
  input[1].revents = 0;
  signal(SIGUSR1, sig_handler_cont);
    
  while(1){
    

    //setup the poll to poll in the stdin
    input[0].fd = STDIN_FILENO;
    input[0].events = POLL_IN;
    ret_poll = poll(input, numfds, -1);

    //this part will be called when there's a new switch trying to connect to
    //the controller. It will place the new switch into the poll queue
    //and increase the queue by 1. We cannot have a queue greater than 7.
    if ((numfds <= sw+1) && (input[1].revents & POLLIN)){
      sw_len = sizeof(sw_addr);
      sw_fd[numfds] = accept(cont_fd, (struct sockaddr *)&sw_addr, &sw_len);
      if ( (sfpin[numfds] = fdopen ( sw_fd[numfds], "r" )) < 0) {
	fprintf (stderr, "%s: fdopen \n", argv[0]);
	exit (1);
      }
      input[numfds].fd = sw_fd[numfds];
      input[numfds].events = POLL_IN;
      input[numfds].revents = 0;
      numfds++;
    }

    //check to see what switch is connecting to the controller.
    for(i = 2; i < numfds; i++){
      if (input[i].revents & POLLIN) {
	ioctl(input[i].fd, FIONREAD, &nread);

	//This if statement will execute if we've lost a connection
	if (nread == 0){
	  //close the poll
	  close(input[i].fd);
	  input[i].events = 0;
	  for (j = 0; j < 7; j++){
	    if (admitted[j] == i){
	      printf("\n** Lost connection to sw%d\n\n", j+1);
	      memset ((char *) &Switches[j].port3, 0, sizeof Switches[j].port3);
	      admitted[j] = 0;
	    }
	    //reset all the admitted flags
	    if (admitted[j] != i && admitted[j] > i)
	      admitted[j]--;
	  }
	  //decrease the poll queue by 1
	  for (j = i; j < numfds; j++){
	    input[j] = input[j+1];
	  }
	  numfds--;
	}
	
	//if we've received a message
	else {
	  for (j = 0; j < 1000; j++)
	    sw2cont[j] = 0;
	  
	  //read the message
	  if(read(sw_fd[i], sw2cont, 1000) < 0) 
	    fprintf(stderr, "%s errno:%d %s", argv[0],errno,strerror(errno));

	  printf("Received %s\n", sw2cont);
	  j=0;
	  while(!isdigit(sw2cont[j])) j++;
	  sw_in = sw2cont[j]-'0';
	  while(sw2cont[j] != '[') j++;

	

	  //check to see if this is an open packet
	  strcpy(s, "[OPEN]");
	  k = 0;
	  found = 1;

	
	  while (s[k]!= 0){
	    if (sw2cont[j] != s[k]){
	      found = 0;
	    }
	      j++;
	      k++;
	  }
	  if(found) opn+=1;
	  //if found and the switch hasn't been admitted, we acknowledge it.
	  if(found && !admitted[sw_in-1]){
	    admitted[sw_in-1] = i;

	    //interpret open command, and add this switch to the
	    //struct swi switches[i-1]

	    //get port1
	    while (sw2cont[j] != '1')
	      j++;
	    j = j+5;
	    if (!isdigit(sw2cont[j]))
	      Switches[sw_in-1].port1 = -1;
	    else
	      Switches[sw_in-1].port1 = sw2cont[j] - '0';

	    //get port2
	    while (sw2cont[j] != '2')
	      j++;
	    j = j+5;
	    if (!isdigit(sw2cont[j]))
	      Switches[sw_in-1].port2 = -1;
	    else
	      Switches[sw_in-1].port2 = sw2cont[j] - '0';

	    //get port3
	    while (sw2cont[j] != '3')
	      j++;
	    j = j+3;
	    Switches[sw_in-1].port3[0] = sw2cont[j];
	    k=0;
	    while(sw2cont[j] != 0){
	      j++;
	      k++;
	      Switches[sw_in-1].port3[k] = sw2cont[j];
	    }


	    //transmit the ack message back to the switch who called open
	    sprintf(s, "(src = cont, dest = sw%d) ", sw_in);
	    strcat(s, "[ACK]");
	    printf("Transmitted %s\n", s);
	    ack++;
	    send(sw_fd[i], s, strlen(s), 0);
	  }

	  //check to see if the message is a query message
	  strcpy(s, "[QUERY]");
	  j = 0;
	  while(sw2cont[j] != '[') j++;
	    
	  k = 0;
	  found = 1;

	
	  while (s[k]!= 0){
	    if (sw2cont[j] != s[k])
	      found = 0;
	    j++;
	    k++;
	    
	  }

	
	  if (found){
	    qry++;
	  
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
		s[k] = 0;
		k++;
		l=0;
		while(isdigit(Switches[j].port3[k])){
		  c[l] = Switches[j].port3[k];
		  l++;
		  k++;
		}
		c[l] = 0;

		IPLOW = atoi(s);
		IPHIGH = atoi(c);

		if(dest <= IPHIGH && dest >= IPLOW){
		  action = j+1;
		  break;
		}
	      }
	    }
	    sprintf(message, "(src = cont, dest = sw%d) ", sw_in);

	    //send an add message back to the switch which queried.
	    strcat(message, "[ADD]\n\t(srcIP= 0-1000, destIP= ");

	    //If there are any ports which the destination IP falls within range
	    //we simply just make the message send a forward message.
	    if(action > 0){
	      arr[0] = '0' + action;
	      arr[1] = 0;
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
	    printf("Transmitted %s\n", message);
	    add++;
	    send(sw_fd[i], message, strlen(message), 0);
	  }
	}
      }
    }
      
    
    
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
      line:
	j = 0;
	for (i=0; i<7; i++)
	  if(Switches[i].port3[0] != 0)
	    j++;
	printf("\n\nSwitch information (nSwitch= %d):\n", j);
	for (i=0; i<7; i++){
	  if (admitted[i])
	    printf("[sw%d] port1= %d, port2= %d, port3= %s\n", i+1, Switches[i].port1, Switches[i].port2, Switches[i].port3);
	}
	printf("\nPacket Stats:\n");
	printf("Received:\tOPEN:%d,\tQUERY:%d\n",opn,qry);
	printf("Transmitted:\tACK:%d,\tADD:%d\n\n",ack,add);
      }

      else printf("Invalid command.\n");
    }
	
  }
  
}

    

int main(int argc, char *argv[]){
  int cont=0, sw=0, *sw_port, port;
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
    sw_port = error_check_cont(argc, argv);
    if(sw_port == NULL) return 0;
    controller(*sw_port, *(sw_port+1), argc, argv);
    return 0;
  }
  
  //switch
  else {
    FILE *fp = error_check_switch(argc, argv);
    if (fp == NULL) return 0;
    port = error_check_port(argv);
    if (port == -1) return 0;
    swich(argc, argv, fp);
    return 0;
  }
}
