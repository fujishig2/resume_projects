#ifndef INTERP_FILE
#define INTERP_FILE
#include "globals.h"

struct Tuple interp_file(FILE *fp);
void create_task(void);
void res_decipher(struct resources *res);

#endif
