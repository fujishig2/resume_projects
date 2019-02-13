#include <sys/stat.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>

void main(void){
  char s[10];
  int i, j;
  for (i=0; i<8; i++){
    for(j=0; j<8; j++){
      if(i != j){
	strcpy(s, "fifo-");
	s[5] = i + '0';
	s[6] = '-';
	s[7] = j + '0';
	s[8] = 0;
	mkfifo(s, S_IWUSR | S_IRUSR | S_IRGRP | S_IWGRP | S_IROTH);
      }
    }
  }
}
	  
      
