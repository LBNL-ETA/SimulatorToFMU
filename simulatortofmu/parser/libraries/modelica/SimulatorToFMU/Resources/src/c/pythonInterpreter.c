/* ENABLE FOR DEBUGGING (VISUAL STUDIO)*/
/* #define _CRTDBG_MAP_ALLOC*/
/* #include <stdlib.h>*/
/* #include <crtdbg.h>*/
#include "pythonInterpreter.h"
#define MAX_PATHNAME_LEN 2048
#define STR_FLAG 1
#define DBL_FLAG 0

#ifdef __APPLE__
#include <crt_externs.h>
#define environ (*_NSGetEnviron())
#else
	extern char **environ;
#endif

/*
 * Replace a string with a character.
 *
 * @param orig Path to a script which is in
 * @param rep Path to a script which is in
 * @param with
 *
 */
/* Replace a character in a string. */
/* You must free the result if result is non-NULL.*/
	char *str_replace(char *orig, char *rep, char *with) {
		char *result; /* the return string */
		char *ins;    /* the next insert point */
		char *tmp;    /* varies */
		int len_rep;  /* length of rep (the string to remove) */
		int len_with; /* length of with (the string to replace rep with) */
		int len_front; /* distance between rep and end of last rep */
		int count;    /*number of replacements */

		/* sanity checks and initialization */
		if (!orig || !rep)
			return NULL;
		len_rep = strlen(rep);
		if (len_rep == 0)
			return NULL; /* empty rep causes infinite loop during count*/
		if (!with)
			with = "";
		len_with = strlen(with);

		/* count the number of replacements needed*/
		ins = orig;
		for (count = 0; tmp = strstr(ins, rep); ++count) {
			ins = tmp + len_rep;
		}
		tmp = result = malloc(strlen(orig) + (len_with - len_rep) * count + 1);
		if (!result)
			return NULL;

		/* first time through the loop, all the variable are set correctly */
		/* from here on, */
		/*    tmp points to the end of the result string */
		/*    ins points to the next occurrence of rep in orig */
		/*    orig points to the remainder of orig after "end of rep" */
		while (count--) {
			ins = strstr(orig, rep);
			len_front = ins - orig;
			tmp = strncpy(tmp, orig, len_front) + len_front;
			tmp = strcpy(tmp, with) + len_with;
			orig += len_front + len_rep; /* move to next "end of rep" */
		}
		strcpy(tmp, orig);
		return result;
	}


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
  cPtr* ptr = malloc(sizeof(cPtr));
  char patDir[MAX_PATHNAME_LEN];
  char base [MAX_PATHNAME_LEN];
  char ext [40];
  int retVal;
  char* conFil="server_config.txt";
  char* batFil="start_server.bat";
  char tmp3[1000];

  /* Split the path to extract the directory name*/ 
  /* retVal=_splitpath_s(str_replace(resScri, "\\", "/"), base, sizeof(base), 
	  patDir, sizeof(patDir), NULL, 0, NULL, 0); */
  retVal=_splitpath_s(resScri, base, sizeof(base), 
	  patDir, sizeof(patDir), NULL, 0, NULL, 0);
  if(retVal!=0){
	  fprintf(stderr, "Python script %s could not be splitted. "
		  "The error code is %d\n", resScri, retVal);
  }

  /* Construct the path to the configuration file */

  /* Set ptr to null as pythonExchangeValuesNoModelica is checking for this */
  ptr->fulScriPat=(char*)malloc((strlen(patDir)+strlen(base) + 10)*sizeof(char));
  sprintf(ptr->fulScriPat, "%s%s", base, patDir);


  ptr->conFilPat=(char*)malloc((strlen(ptr->fulScriPat)+strlen(conFil)+1)*sizeof(char));
  ptr->batFilPat=(char*)malloc((strlen(ptr->fulScriPat)+strlen(batFil)+10)*sizeof(char));
  sprintf(ptr->conFilPat, "%s%s", ptr->fulScriPat, conFil);
  printf("This is the path to the configuration file %s\n", ptr->conFilPat);
  sprintf(ptr->batFilPat, "%s%s", ptr->fulScriPat, batFil);
  printf("This is the path to the batch file file %s\n", ptr->batFilPat);
  
  /* Start the server in  a non-blocking mode */
  pid=(HANDLE)_spawnl(P_NOWAIT,  ptr->batFilPat,  ptr->batFilPat, 
  	  ptr->fulScriPat, NULL); 
  /* Needs to wait that the server is up*/
  //sprintf(tmp3, "%s%s%s%s", "start ", "C:\\Users\\Public\\start_server.bat", " ", "C:\\Users\\Public\\");
  //system (tmp3);
  Sleep(1000);
  ptr->ptr = NULL;
  ptr->isInitialized = 0;
  ptr->pModule = NULL;
  ptr->pFunc = NULL;
  ptr->patDir = (char *)malloc((strlen(ptr->fulScriPat) + 50)*sizeof(char));
  if (!Py_IsInitialized())
	Py_Initialize();
  	PyRun_SimpleString("import sys");
	sprintf(ptr->patDir, "%s%s%s%s%s", "sys.path.append(", "\"", ptr->fulScriPat, "\"", ")");
	PyRun_SimpleString(ptr->patDir);
  return (void*) ptr;
}

static size_t
WriteMemoryCallback(void *contents, size_t size, size_t nmemb, void *userp)
{
  size_t realsize = size * nmemb;
  struct MemoryStruct *mem = (struct MemoryStruct *)userp;
 
  mem->memory = realloc(mem->memory, mem->size + realsize + 1);
  if(mem->memory == NULL) {
    /* out of memory! */ 
    printf("not enough memory (realloc returned NULL)\n");
    return 0;
  }
 
  memcpy(&(mem->memory[mem->size]), contents, realsize);
  mem->size += realsize;
  mem->memory[mem->size] = 0;
  return realsize;
}



/*
 * Function to join an array of strings                            
 * this function allocates memory that must be freed by the caller 
 *
 * @param strings the string array to join 
 * @param count the number of elements

 */
char* join_strings(char *strings[], int count)
{
  char* str = NULL;             /* Pointer to the joined strings  */
  size_t total_length = 0;      /* Total length of joined strings */
  size_t length = 0;            /* Length of a string             */
  int i = 0;                    /* Loop counter                   */

  /* Find total length of joined strings */
  for(i = 0 ; i<count ; i++)
  {
    total_length += strlen(strings[i]);
    if(strings[i][strlen(strings[i])-1] != '\n')
      ++total_length; /* For newline to be added */
  }
  ++total_length;     /* For joined string terminator */

  str = (char*)malloc(total_length);  /* Allocate memory for joined strings */
  str[0] = '\0';                      /* Empty string we can append to      */

  /* Append all the strings */
  for(i = 0 ; i<count ; i++)
  {
    strcat(str, strings[i]);
    length = strlen(str);

    /* Check if we need to insert newline */
    if(str[length-1] != '\n')
    {
      str[length] = ',';             /* Append a newline       */
      str[length+1] = '\0';           /* followed by terminator */
    }
  }
  return str;
}

/*
 * This function exchanges variables with an 
 * external simulator. 
 *
 * @param moduleName the module name 
 * @param functionName the function name
 * @param configFileName the configuration file
 * @param modTim the simulation time
 * @param nDblWri the number of double variables to write
 * @param strWri the string variables to write
 * @param dblValWri the double values to write
 * @param nDblRea the number of variables to read
 * @param strRea the string variables to read
 * @param dblValRea the double values to read
 * @param nDblParWri the number of parameters to write
 * @param strParWri the string parameters to write
 * @param dblValParWri the double parameters to write
 * @param resWri the result flag
 * @param ModelicaFormatError the pointer
 * to the ModelicaFormatError
 * @param memory a Python object               
 * @param have_memory the flag indicating a Python object   
 */
void pythonExchangeVariables(const char * moduleName,
	const char * functionName,
	const char * configFileName,
	double modTim,
	const size_t nDblWri, 
	const char ** strWri, 
	double * dblValWri, 
	size_t nDblRea, 
	const char ** strRea,
	double * dblValRea, 
	size_t nDblParWri, 
	const char ** strParWri, 
	double * dblValParWri, 
	int resWri,
	void (*ModelicaFormatError)(const char *string,...),
	void* memory, int passPythonObject){

	CURL *curl_handle;
    CURLcode res;
 
    struct MemoryStruct chunk;
	int nRea;

	char* arg="";
	char buf[1024];
	FILE *fil;
	char* address;
	char* port;
	char* token;
	char** tmpInVal;
	int i;
	char time_str[100];
	char* url_str;

  	cPtr* cMemory = (cPtr*)memory;

	const char *confFilNam [] = {configFileName};
	 
    chunk.memory = malloc(1);  /* will be grown as needed by the realloc above */ 
    chunk.size = 0;    /* no data at this point */ 

	if (cMemory->isInitialized==0) {
		/*  fixme cMemory->inNam to be freed*/
		cMemory->inNam = (char*)malloc((nDblWri*500)*sizeof(char));
		/*  fixme cMemory->inNam to be freed*/
		cMemory->inVal = (char*)malloc((nDblWri*500)*sizeof(char));
		/*  fixme cMemory->outNam to be freed*/
		cMemory->outNam = (char*)malloc((nDblRea*500)*sizeof(char));
		/* Open configuration and read token */
		fil = fopen(cMemory->conFilPat, "r");
		if (fil) {
			while ((nRea = fread(buf, 1, sizeof buf, fil)) > 0)
				continue;
			if (ferror(fil)) {
				(*ModelicaFormatError)("Failed to read configuration file '%s'.\n", 
					cMemory->conFilPat);
			}
			fclose(fil);
		}
		
		/* Extract the port and the address */
		token = strtok(buf, ":");
		while(token!=NULL){
			if (strstr(token, "address")){
				token = strtok(NULL, ":");
				cMemory->address=token;
			}
			if (strstr(token,"port")){
				token = strtok(NULL, ":");
				cMemory->port=token;
			}
			token = strtok(NULL, ":");
		}
		printf("This is the address retrieved %s and the port=%s\n", cMemory->address, cMemory->port);
		
		/* Join the strings and do not forget to free the join_strings, basicall free cMemory->inNam when done*/
		strcpy(cMemory->inNam, join_strings(strWri, nDblWri));
		cMemory->inNam[strlen(cMemory->inNam)-1]=0;
		printf ("This is the string to write %s\n", cMemory->inNam);


		/* Join the strings and do not forget to free the join_strings, basicall free cMemory->outNam when done*/
		strcpy(cMemory->outNam, join_strings(strRea, nDblRea));
		cMemory->outNam[strlen(cMemory->outNam)-1]=0;
		printf ("This is the string to write %s\n", cMemory->outNam);
	}
	

    /* Convert the doubles values into doubles strings and then convert the string into a single string*/
	tmpInVal = (char**)malloc(nDblWri*sizeof(char*));
	for (i=0; i<nDblWri; i++){
		tmpInVal[i] = (char*)malloc(100*sizeof(char));
		sprintf(tmpInVal[i], "%.8f", dblValWri[i]);
		printf ("This is the string to write %s\n", tmpInVal[i]);
	}

	/* Join the strings and do not forget to free the join_strings, basicall free cMemory->inVal when done*/
	strcpy(cMemory->inVal, join_strings(tmpInVal, nDblWri));
	cMemory->inVal[strlen(cMemory->inVal)-1]=0;
	printf ("This is the string to write %s\n", cMemory->inVal);

	/* Ready to send data to the server */
	curl_global_init(CURL_GLOBAL_ALL);

	/* init the curl session */ 
	curl_handle = curl_easy_init();

	/* init the curl session */ 
	curl_handle = curl_easy_init();

	/* Convert time in string*/
	sprintf(time_str, "%.5f", time);

	url_str=(char*)malloc((strlen(cMemory->address)+
		strlen(cMemory->port)+strlen(cMemory->inNam)+
		strlen(cMemory->inVal)+strlen(cMemory->outNam)+
		strlen(time_str)+100)*sizeof(char));
	sprintf(url_str, "%s%s%s%s%s%s%s%s%s%s%s%s%s%s", "http://", 
		cMemory->address, ":", cMemory->port, "/", "dostep", "/", 
		time_str, "&", cMemory->inNam, "&", cMemory->inVal, "&", 
		cMemory->outNam);
	printf("This is the character to send %s\n", url_str);

	/* specify URL to get */ 
	curl_easy_setopt(curl_handle, CURLOPT_URL, url_str);

	/* send all data to this function  */ 
	curl_easy_setopt(curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);

	/* we pass our 'chunk' struct to the callback function */ 
	curl_easy_setopt(curl_handle, CURLOPT_WRITEDATA, (void *)&chunk);

	/* some servers don't like requests that are made without a user-agent
	 * field, so we provide one */ 
	/* curl_easy_setopt(curl_handle, CURLOPT_USERAGENT, "libcurl-agent/1.0"); */

	/* get it! */ 
	res = curl_easy_perform(curl_handle);

	//* check for errors */ 
	if(res != CURLE_OK) {
		fprintf(stderr, "curl_easy_perform() failed: %s\n",
			curl_easy_strerror(res));
		 (*ModelicaFormatError)("curl_easy_perform() failed: %s\n",
			curl_easy_strerror(res));
	}
	else {
		/*
		* Now, our chunk.memory points to a memory block that is chunk.size
		* bytes big and contains the remote file.
		*/ 
		/* Error handling done by checking first character of the message. */
		if(chunk.memory[0]=='E' || chunk.memory[0]=='e'){
			(*ModelicaFormatError)("Failed to get the data at time %f. %s\n", time,  
				chunk.memory);
		}
		token = strtok(chunk.memory, ",");
		i=0;
		while (token != NULL)
		{
			dblValRea[i]=strtod(token, NULL);
			printf ("This is the return value %f\n", dblValRea[i]);
			i++;
			token = strtok(NULL, ",");
		}
	}
 
	/* cleanup curl stuff */ 
	curl_easy_cleanup(curl_handle);
	free(chunk.memory);

	/* we're done with libcurl, so clean it up */ 
	curl_global_cleanup();
	
	/* Free memory */
	for (i=0; i<nDblWri; i++){
		free(tmpInVal[i]);
	}
	free(tmpInVal);	
	return;
}

/*
// 3/26/2013- TN: checkStringLength is commented out since it is not used.
void checkStringLength(const char * str, size_t strLen){
int i;
int n;

n = -1;
for(i = 0; i < strLen+1; i++){
if (str[i] == '\0'){
n = i;
break;
}
}
if (n == -1)
//    ModelicaFormatError("String %.2s has more than %d characters. Increase parameter strLen.",
ModelicaFormatError("String %s has more than %d characters. Increase parameter strLen.",
str, strLen);
return;
}
*/
void freePythonMemory(void* object)
{
  if ( object != NULL ){
    cPtr* p = (cPtr*) object;
	free(p->patDir);
	free(p->inNam);
	free(p->outNam);
	free(p->inVal);
    free(p);
  }
}
