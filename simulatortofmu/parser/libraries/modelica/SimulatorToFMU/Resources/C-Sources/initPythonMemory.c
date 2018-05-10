#ifdef _MSC_VER
#include <process.h>
#include <windows.h>
#endif
#define MAX_PATHNAME_LEN 2048

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

/*
 * Start the server FMU.
 *
 * @param resScri Path to a script which is in
 * the resource folder of the FMU.
 */
void* initPythonMemory(char* resScri)
{
#ifdef _MSC_VER
	HANDLE  pid;
#else
	pid_t  pid;
#endif
  cPtr* ptr = (cPtr*)malloc(sizeof(cPtr));
  char patDir[MAX_PATHNAME_LEN];
  char base [MAX_PATHNAME_LEN];
  char ext [40];
  int retVal;
  char* conFil="server_config.txt";
  char* batFil="start_server.bat";
  char* tmpScri;
  char* token;
  FILE* fil;
  char buf[1024];
  int nRea;

  /* Split the path to extract the directory name*/
  /* retVal=_splitpath_s(str_replace(resScri, "\\", "/"), base, sizeof(base),
	  patDir, sizeof(patDir), NULL, 0, NULL, 0); */
#ifdef _MSC_VER
    /* Check for case where we have UNC path*/
    /* if(resScri[0]=="\\"){ */
      tmpScri=(char*)malloc(strlen(resScri)*sizeof(char));
      memcpy(tmpScri, resScri+4, strlen(resScri+4));
      retVal=_splitpath_s(tmpScri, base, sizeof(base),
        patDir, sizeof(patDir), NULL, 0, NULL, 0);
        if(retVal!=0){
          ModelicaFormatError("Python script %s could not be splitted. "
            "The error code is %d\n", tmpScri, retVal);
        }
    /*  }
    // else{
    //   retVal=_splitpath_s(resScri, base, sizeof(base),
    //     patDir, sizeof(patDir), NULL, 0, NULL, 0);
    //     if(retVal!=0){
    //       ModelicaFormatError("Python script %s could not be splitted. "
    //         "The error code is %d\n", resScri, retVal);
    //     }
    // } */
#endif

  /* Construct the path to the configuration file */
  ptr->fulScriPat=(char*)malloc((strlen(patDir)+strlen(base) + 10)*sizeof(char));
  sprintf(ptr->fulScriPat, "%s%s", base, patDir);
  ptr->address=(char*)malloc(100*sizeof(char));
  ptr->port=(char*)malloc(100*sizeof(char));

  ptr->conFilPat=(char*)malloc((strlen(ptr->fulScriPat)+strlen(conFil)+1)*sizeof(char));
  ptr->batFilPat=(char*)malloc((strlen(ptr->fulScriPat)+strlen(batFil)+10)*sizeof(char));
  sprintf(ptr->conFilPat, "%s%s", ptr->fulScriPat, conFil);
  ModelicaFormatMessage("This is the path to the configuration file %s\n", ptr->conFilPat);
  sprintf(ptr->batFilPat, "%s%s", ptr->fulScriPat, batFil);
  ModelicaFormatMessage("This is the path to the full script file %s\n", ptr->fulScriPat);

  /* Start the server in  a non-blocking mode */
  pid=(HANDLE)_spawnl(P_NOWAIT,  ptr->batFilPat,  ptr->batFilPat,
  	  ptr->fulScriPat, NULL);
  /* Needs to wait that the server is up*/
  /* sprintf(tmp3, "%s%s%s%s", "start ", ptr->batFilPat, " ", ptr->fulScriPat); */
  /* system (tmp3); */
#ifdef _MSC_VER
  Sleep(10000);
#endif
  /* Open configuration and read token */
  fil = fopen(ptr->conFilPat, "r");
  if (fil) {
    while ((nRea = fread(buf, 1, sizeof buf, fil)) > 0)
      continue;
    if (ferror(fil)) {
      (*ModelicaFormatError)("Failed to read configuration file '%s'.\n",
        ptr->conFilPat);
    }
    fclose(fil);
  }

  /* Extract the port and the address */
  token = strtok(buf, ":");
  while(token!=NULL){
    if (strstr(token, "address")){
      token = strtok(NULL, ":");
      sprintf(ptr->address, "%s", token);
    }
    if (strstr(token,"port")){
      token = strtok(NULL, ":");
      sprintf(ptr->port, "%s", token);
      break;
    }
    token = strtok(NULL, ":");
  }

  ptr->isInitialized = 0;
  ptr->patDir = (char *)malloc((strlen(ptr->fulScriPat) + 50)*sizeof(char));
  return (void*) ptr;
}
