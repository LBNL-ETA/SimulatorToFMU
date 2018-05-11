/* ENABLE FOR DEBUGGING (VISUAL STUDIO)*/
/* #define _CRTDBG_MAP_ALLOC*/
/* #include <stdlib.h>*/
/* #include <crtdbg.h>*/
#include "serverInterpreter.h"
#define MAX_PATHNAME_LEN 2048

#ifdef __APPLE__
#include <crt_externs.h>
#define environ (*_NSGetEnviron())
#else
extern char **environ;
#endif

/*
* Replace a string with a character.
*
* @param orig Input string
* @param rep string to replace
* @param with string to replace rep
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
* Start the server FMU.
*
* @param resScri Path to a script which is in
* the resource folder of the FMU.
*/
void* initServerMemory(char* resScri)
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
	/* char tmp3[1000]; */
	char* tmpScri;
	char* token;
	FILE* fil;
	char buf[1024];
	int nRea;
	int nCoun=0;
	int i;
	struct stat sb;

	/* Split the path to extract the directory name*/
#ifdef _MSC_VER
	if(strncmp(resScri, "\\", 1)==0){
		printf("The path to the resource script %s is UNC\n.", resScri);
		for (i=0; i<strlen(resScri); i++){
			if(resScri[i]!=':'){
				nCoun++;
				continue;
			}
			else{
				nCoun--;
				break;
			}
		}

		tmpScri=(char*)malloc((strlen(resScri+nCoun)+1)*sizeof(char));
		strncpy(tmpScri, resScri+nCoun, strlen(resScri+nCoun));

		retVal=_splitpath_s(tmpScri, base, sizeof(base),
			patDir, sizeof(patDir), NULL, 0, NULL, 0);
	}
	else{
		retVal=_splitpath_s(resScri, base, sizeof(base),
			patDir, sizeof(patDir), NULL, 0, NULL, 0);
	}


	if(retVal!=0){
		fprintf(stderr, "The path to the resource script %s could not be splitted. "
			"The error code is %d\n.", resScri, retVal);
		exit(1);
	}
#endif
	/* Construct the path to the configuration file */
	ptr->fulScriPat=(char*)malloc((strlen(patDir)+strlen(base) + 10)*sizeof(char));
	sprintf(ptr->fulScriPat, "%s%s", base, patDir);
#ifdef _MSC_VER
	/* Changed separator to check validity of path */
	str_replace(ptr->fulScriPat, "\\", "\\\\");
#endif
	if (!stat(ptr->fulScriPat, &sb)){
		fprintf(stderr, "The path to resource folder %s doesn't exist.", ptr->fulScriPat);
		exit(1);
	}
	ptr->address=(char*)malloc(100*sizeof(char));
	ptr->port=(char*)malloc(100*sizeof(char));

	ptr->conFilPat=(char*)malloc((strlen(ptr->fulScriPat)+strlen(conFil)+1)*sizeof(char));
	ptr->batFilPat=(char*)malloc((strlen(ptr->fulScriPat)+strlen(batFil)+10)*sizeof(char));
	sprintf(ptr->conFilPat, "%s%s", ptr->fulScriPat, conFil);
	printf("The path to the configuration file is %s\n.", ptr->conFilPat);
	sprintf(ptr->batFilPat, "%s%s", ptr->fulScriPat, batFil);
	printf("The path to the batch file is %s\n.", ptr->batFilPat);

	/* Start the server in  a non-blocking mode */
	pid=(HANDLE)_spawnl(P_NOWAIT,  ptr->batFilPat,  ptr->batFilPat,
		ptr->fulScriPat, NULL);
#ifdef _MSC_VER
	Sleep(5000);
#endif

	/* Open configuration and read token */
	fil = fopen(ptr->conFilPat, "r");
	if (fil) {
		while ((nRea = fread(buf, 1, sizeof buf, fil)) > 0)
			continue;
		if (ferror(fil)) {
			fprintf(stderr, "Failed to read configuration file '%s'.\n",
				ptr->conFilPat);
			exit(1);
		}
		fclose(fil);
	}

	/* Extract the port and the address */
	token = strtok(buf, ":");
	while(token!=NULL){
		if (strstr(token, "address")){
			token = strtok(NULL, ":");
			sprintf(ptr->address, "%s", token);
			printf("The server address is %s\n.", ptr->address);
		}
		if (strstr(token,"port")){
			token = strtok(NULL, ":");
			sprintf(ptr->port, "%s", token);
			printf("The server port is %s\n.", ptr->port);
			break;
		}
		token = strtok(NULL, ":");
	}

	ptr->ptr = NULL;
	ptr->isInitialized = 0;
	free(ptr->conFilPat);
	free(ptr->batFilPat);
	free( ptr->fulScriPat);
	return (void*) ptr;
}

/*
* This function exchanges variables with an
* external simulator.
*
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
* @param memory a Server object
*/
void serverExchangeVariables(
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
	void* memory){

		CURLcode res;
		int i;
		struct MemoryStruct chunk;
		char* token;
		char** tmpInVal;
		char time_str[100];
		char* url_str;

		cPtr* cMemory = (cPtr*)memory;
		const char *confFilNam [] = {configFileName};
		chunk.memory = malloc(1);  /* will be grown as needed by the realloc above */
		chunk.size = 0;    /* no data at this point */

		if (cMemory->ptr==NULL){
			cMemory->inVal = (char*)malloc((nDblWri*500)*sizeof(char));
			cMemory->inNam = (char*)malloc((nDblWri*500)*sizeof(char));
			cMemory->outNam = (char*)malloc((nDblRea*500)*sizeof(char));

			/* Join the strings */
			sprintf(cMemory->inNam, "%s", join_strings(strWri, nDblWri));
			cMemory->inNam[strlen(cMemory->inNam)-1]=0;

			/* Join the strings */
			sprintf(cMemory->outNam, "%s", join_strings(strRea, nDblRea));
			cMemory->outNam[strlen(cMemory->outNam)-1]=0;

			/* Initialize global session */
			curl_global_init(CURL_GLOBAL_ALL);

			/* init the curl session */
			cMemory->curl_handle = curl_easy_init();
		}

		/* Convert the doubles values into doubles strings and then convert the string into a single string*/
		tmpInVal = (char**)malloc(nDblWri*sizeof(char*));
		for (i=0; i<nDblWri; i++){
			tmpInVal[i] = (char*)malloc(100*sizeof(char));
			sprintf(tmpInVal[i], "%.8f", dblValWri[i]);
		}

		/* Join the strings */
		sprintf(cMemory->inVal, "%s", join_strings(tmpInVal, nDblWri));
		cMemory->inVal[strlen(cMemory->inVal)-1]=0;

		/* Convert time in string*/
		sprintf(time_str, "%.5f", time);

		url_str=(char*)malloc((strlen(cMemory->address)+
			strlen(cMemory->port)+strlen(cMemory->inNam)+
			strlen(cMemory->inVal)+strlen(cMemory->outNam)+
			strlen(time_str)+100)*sizeof(char));

		/* Write the string to be sent */
		sprintf(url_str, "%s%s%s%s%s%s%s%s%s%s%s%s%s%s", "http://",
			cMemory->address, ":", cMemory->port, "/", "dostep", "/",
			time_str, "&", cMemory->inNam, "&", cMemory->inVal, "&",
			cMemory->outNam);

		/* specify URL to get */
		curl_easy_setopt(cMemory->curl_handle, CURLOPT_URL, url_str);

		/* send all data to this function  */
		curl_easy_setopt(cMemory->curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);

		/* we pass our 'chunk' struct to the callback function */
		curl_easy_setopt(cMemory->curl_handle, CURLOPT_WRITEDATA, (void *)&chunk);

		/* some servers don't like requests that are made without a user-agent
		* field, so we provide one */
		/* curl_easy_setopt(cMemory->curl_handle, CURLOPT_USERAGENT, "libcurl-agent/1.0"); */

		/* get the values from the server */
		res = curl_easy_perform(cMemory->curl_handle);

		/* check for errors */
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
				i++;
				token = strtok(NULL, ",");
			}
		}

		/* Free variables which will be reconstructed */
		for (i=0; i<nDblWri; i++){
			free(tmpInVal[i]);
		}
		free(tmpInVal);

		free(url_str);
		free(chunk.memory);
		cMemory->isInitialized=1;
		memory = cMemory;
		cMemory->ptr=memory;
		return;
}

void freeServerMemory(void* object)
{
	if ( object != NULL ){
		cPtr* p = (cPtr*) object;
		free(p->inVal);
		free(p->outNam);
		free(p->inNam);
		curl_easy_cleanup(p->curl_handle);
		curl_global_cleanup();
		free(p);
	}
}

