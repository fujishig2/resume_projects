#ifndef GLOBALS
#include "globals.h"
#endif

#ifndef INTERP_FILE
#define INTERP_FILE

struct Tuple interp_file(FILE *fp);
void create_task(void);
void res_decipher(struct resources *res);

#endif
