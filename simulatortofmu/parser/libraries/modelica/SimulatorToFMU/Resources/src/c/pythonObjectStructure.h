/*
 * A structure to store a pointer that is used
 * to point to a Python object between the function
 * invocations.
 *
 * Michael Wetter, LBNL                                1/31/2018
 */

#ifndef BUILDINGS_PYTHONOBJECTSTRUCTURE_H /* Not needed since it is only a typedef; added for safety */
#define BUILDINGS_PYTHONOBJECTSTRUCTURE_H

#ifdef __APPLE__
#include <Python/Python.h>
#else
#include <Python.h>
#endif

typedef struct cPtr
{
  void* ptr;
  char* patDir;
  char* conFilPat;
  char* batFilPat;
  char* fulScriPat;
  char* address;
  char* port;
  char* inNam;
  char* inVal;
  char* outNam;
  int isInitialized;
} cPtr;


#endif
