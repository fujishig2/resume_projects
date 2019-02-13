#ifndef CREATE_THREADS
#define CREATE_THREADS

#include "globals.h"

void create_threads(struct Tuple tuple, int monTime, int iter);
void task_mutex_pipe(int stat, int task_no);
void *task_thread(void *task);
void *monitor_thread(void *monTime);

#endif
