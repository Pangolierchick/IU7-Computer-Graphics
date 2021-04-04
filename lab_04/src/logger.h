#ifndef __LOGGER_H__
#define __LOGGER_H__

#include <cstdio>

#define VERSION              "0.5"

#define LOG_LEVEL           4

#define NO_LOG              0
#define ERROR               1
#define INFO                2
#define DEBUG               3
#define TRACE               4

#define INFO_TAG            GREEN "INFO " RESET_COLOR
#define ERROR_TAG           RED "ERROR" RESET_COLOR
#define DEBUG_TAG           YELLOW "DEBUG" RESET_COLOR
#define TRACE_TAG           MAGENTA "TRACE" RESET_COLOR

#define LOGGER_FORMAT(tag)    "[" tag "]" "[%19s] [%17s:%4d] "
#define LOGGER_ARGS()         __FILE__, __func__, __LINE__

#define GENERICK_POINTER(p)             (void *) p

#define MESSAGE_LOG_LEVEL LOG_LEVEL

#if MESSAGE_LOG_LEVEL
#define XSTR(x) STR(x)
#define STR(x)  #x

#pragma message ("Logging level " XSTR(LOG_LEVEL))

#endif 

// ============= COLORS SECTION =============

#define MAGENTA    "\u001b[35;1m"
#define YELLOW      "\u001b[33;1m"
#define GREEN       "\u001b[32;1m"
#define RED         "\u001b[31;1m"
#define RESET_COLOR "\u001b[0m"

// ==========================================


#if LOG_LEVEL >= DEBUG
#define DBG_PRINT(msg, ...)     fprintf(stderr, LOGGER_FORMAT(DEBUG_TAG) msg, LOGGER_ARGS(), ## __VA_ARGS__)
#define DBG_PRINTF(format, ...) fprintf(stderr, format, __VA_ARGS__);
#else
#define DBG_PUTS(msg)
#define DBG_PRINT(...)
#define DBG_PUT(msg)
#define DBG_PRINTF(...)
#endif

#if LOG_LEVEL >= INFO
#define INFO_PRINT(msg, ...)     fprintf(stderr, LOGGER_FORMAT(INFO_TAG) msg, LOGGER_ARGS(), ## __VA_ARGS__)
#define INFO_PRINTF(format, ...) fprintf(stderr, format, __VA_ARGS__);
#else
#define INFO_PRINT(...)
#define INFO_PRINTF(...)
#endif

#if LOG_LEVEL >= ERROR
#define ERROR_PRINT(msg, ...)     fprintf(stderr, LOGGER_FORMAT(ERROR_TAG) msg, LOGGER_ARGS(), ## __VA_ARGS__)
#define ERROR_PRINTF(format, ...) fprintf(stderr, format, __VA_ARGS__);
#else
#define ERROR_PRINT(...)
#define ERROR_PRINTF(...)
#endif

#if LOG_LEVEL >= TRACE
#define TRACE_PRINT(msg, ...)     fprintf(stderr, LOGGER_FORMAT(TRACE_TAG) msg, LOGGER_ARGS(), ## __VA_ARGS__)
#define TRACE_PRINTF(format, ...) fprintf(stderr, format, __VA_ARGS__);
#else
#define TRACE_PRINT(...)
#define TRACE_PRINTF(...)
#endif

#endif // __LOGGER_H__
