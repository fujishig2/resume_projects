#include<stdio.h>
#include<stdbool.h>
int rows, cols, box;

bool recursive_solve(int board[9][9], int position);
void print_board(int board[9][9]);
void read_board(int board[9][9], FILE *fp);
bool check_valid(int board[9][9]);
bool check_nine(int nine[9]);

int main(void)
{
  FILE *fp;
  char file_name[100];
  int board[9][9];
  bool valid = true;
  int position;
  printf("Please enter the sudoku file name (0 = exit): ");
  scanf("%s", file_name);
  fp = fopen(file_name, "r");
  while(fp != NULL){
    position = 0;
    read_board(board, fp);
    valid = check_valid(board);
    if (valid == true){
      valid = recursive_solve(board, position);
      if (valid == true){
	printf("The finished board is:\n");
	print_board(board);
      }
      else printf("This board is invalid!\n");
    }	
    else printf("This board is invalid!\n");
    printf("Please enter the sudoku file name (0 = exit): ");
    scanf("%s", file_name);
    fp = fopen(file_name, "r");
  }
  return 0;
}

bool recursive_solve(int board[9][9], int position){
  if (position < 81){
    int *p;
    int board2[9][9];
    bool valid;
    for(rows = 0; rows < 9; rows++){
      for(cols = 0; cols < 9; cols++){
	board2[rows][cols] = board[rows][cols];
      }
    }
    p = &board2[0][0];
    p = p + position;
    if (*p == 0){
      for (int i = 1; i < 10; i++){
	*p = i;
	valid = check_valid(board2);
	if (valid == true){
	  valid = recursive_solve(board2, position+1);
	  if (valid == true){
	    break;
	  }
	}
      }
    }
    else{
      valid = recursive_solve(board2, position+1);
    }
    if (valid == true){
      for(rows = 0; rows < 9; rows++){
	for(cols = 0; cols < 9; cols++){
	  board[rows][cols] = board2[rows][cols];
	}
      }
    }
    return valid;
  }
  else {
    return true;
  }
}
    


void print_board(int board[9][9]){
  for (rows = 0; rows < 9; rows++){
    for (cols = 0; cols < 9; cols++){
      printf("%d ", board[rows][cols]);
    }
    printf("\n");
  }
  printf("\n\n\n");
}

void read_board(int board[9][9], FILE *fp){
  printf("The starting board is:\n");
  for(rows = 0; rows < 9; rows++){
    for(cols = 0; cols < 9; cols++){
      fscanf(fp, "%d", &board[rows][cols]);
      printf("%d ", board[rows][cols]);
    }
    printf("\n");
  }
  printf("\n\n\n");
  return;
}

bool check_valid(int board[9][9]){
  int nine[9] = {0,0,0,0,0,0,0,0,0};
  bool valid = true;
  for (rows = 0; rows < 9; rows++){
    for (int i = 0; i < 9; i++){
      nine[i] = board[rows][i];
    }
    if (valid == true) valid = check_nine(nine);
    for (cols = 0; cols < 9; cols++){
      nine[cols] = board[cols][rows];
    }
    if (valid == true) valid = check_nine(nine);
    if (rows % 3 == 0){
      for (cols = 0; cols < 9; cols+=3){
	for (box = 0; box < 9; box++){
	  nine[box] = board[rows+box/3][cols + box%3];
	}
	if (valid == true) valid = check_nine(nine);
      }
    }
  }

  if (valid == true) return true;
  else return false;
}

bool check_nine(int nine[9]){
	int a, b;
	for (a = 0; a < 9; a++){
		for(b = a+1; b < 9; b++){
			if(nine[a] == nine[b] && nine[a] > 0){
				return false;
			}
		}
	}
	for (a = 0; a < 9; a++){
		nine[a] = 0;
	}
	return true;
}
