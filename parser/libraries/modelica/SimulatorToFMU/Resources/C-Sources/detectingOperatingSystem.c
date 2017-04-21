/*
 *
 * \file   detectOperatingSystem.c
 *
 * \brief  Detect the operating system
 *
 * \author Thierry S. Nouidui
 *         Lawrence Berkeley National Laboratory
 *         TSNouidui@lbl.gov
 *
 * \date   2/8/2017
 *
 */

/*
 * Detect the operating system and return 0 for Windows 64, 
 * 1 for Windows 32, 2 for Linux 64, and 3 for Linux32
 *
 * @return 0 if Windows 64, 1 if Windows 32, 2 if Linux64, 3 if Linux32
 */

#include <stdio.h>


#if defined(_MSC_VER) || defined(__WIN32__) \
 || defined(_WIN32) || defined(WIN32)  \
 || defined(__CYGWIN__) || defined(__MINGW32__) \
 || defined(__BORLANDC__) /*Windows and MinGW */
#include <windows.h>
#else /* Linux*/
#include <stdint.h> /* Needed to detect 32 vs. 64 bit using UINTPTR_MAX*/
#endif

int detectOperatingSystem() {


#if defined(_MSC_VER) || defined(__WIN32__) \
 || defined(_WIN32) || defined(WIN32)  \
 || defined(__CYGWIN__) || defined(__MINGW32__) \
 || defined(__BORLANDC__) /*Windows and MinGW */

#if _WIN64
  return 0;
#elif _WIN32
  return 1;
#else
  ModelicaError("Error: Failed to detect 32 or 64 bit Windows system in detectOperatingSystem.c.\n");
#endif

#elif __linux__ /*Linux*/
#if UINTPTR_MAX == 0xffffffffffffffff
/* 64-bit */
  return 2;
#elif UINTPTR_MAX == 0xffffffff
/* 32-bit */
  return 3;
#else
  ModelicaError("Error: Failed to detect 32 or 64 bit Linux system in detectOperatingSystem.c.\n");
#endif

#else /* Neither MSC nor Linux */
  ModelicaError("Error: Unsupported operating system in detectOperatingSystem.c.\n");
#endif
} /* End of detectOperatingSystem()*/
