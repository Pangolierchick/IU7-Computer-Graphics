#pragma once 

#include <stdint.h>
#include <stdio.h>
#include <time.h>

extern struct timespec start_time_s, end_time_s; // for timer purposes

// CLOCK_REALTIME
// CLOCK_PROCESS_CPUTIME_ID

#define START_MEASURING() clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &start_time_s);
#define END_MEASURING() clock_gettime(CLOCK_PROCESS_CPUTIME_ID, &end_time_s);

#define SHOW_TIME(msg) printf ("\n\n\x1b[33m" msg "\033[0m %lds %ldns\n", end_time_s.tv_sec - start_time_s.tv_sec, labs(end_time_s.tv_nsec - start_time_s.tv_nsec))
#define GET_SEC() ((end_time_s.tv_sec - start_time_s.tv_sec) * 10*6)
#define GET_NSEC() ((end_time_s.tv_nsec - start_time_s.tv_nsec) / 1e3)

#define GET_TIME() (GET_SEC() + GET_NSEC())
