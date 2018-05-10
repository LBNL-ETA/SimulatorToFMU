/*
 * A structure to store a pointer that is used
 * to point to a C object between the function
 * invocations.
 *
 * Thierry S. Nouidui, LBNL                                5/06/2018
 */

#ifndef BUILDINGS_PYTHONOBJECTSTRUCTURE_H /* Not needed since it is only a typedef; added for safety */
#define BUILDINGS_PYTHONOBJECTSTRUCTURE_H

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
  char** tmpInVal;
  int isInitialized;
} cPtr;


#endif
