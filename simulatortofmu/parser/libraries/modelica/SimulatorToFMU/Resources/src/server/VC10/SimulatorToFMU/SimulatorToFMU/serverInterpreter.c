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
* @param patConFil Path to configuration file
*
*/
void* initServerMemory(char* resScri, size_t nStrPar, size_t nDblPar, char** strParNam, 
	char** strParVal, char** dblParNam, double* dblParVal)
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
	char* cheSer="check_server.py";
	char* tmpScri;
	char* token;
	FILE* fil;
	char buf[1024];
	int nRea;
	int nCoun=0;
	int i;
	struct stat sb;
	char* url_str;
	CURLcode res;
	float inc=0;
	char str[MAX_PATHNAME_LEN];
	char** tmpDblParVal;
	struct MemoryStruct chunk;
	chunk.memory = (char*)malloc(sizeof(char)*10000);  /* will be grown as needed by the realloc above */
	chunk.size = 0;    /* no data at this point */
	

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
	printf("The full script path is %s\n", ptr->fulScriPat);
	/*fixme: This is not checking the path correctly*/
	/*if (!stat(ptr->fulScriPat, &sb)){
		fprintf(stderr, "The path to resource folder %s doesn't exist.", ptr->fulScriPat);
		exit(1);
	}
	*/
	ptr->address=(char*)malloc(100*sizeof(char));
	ptr->port=(char*)malloc(100*sizeof(char));

	ptr->conFilPat=(char*)malloc((strlen(ptr->fulScriPat)+strlen(conFil)+1)*sizeof(char));
	ptr->batFilPat=(char*)malloc((strlen(ptr->fulScriPat)+strlen(batFil)+10)*sizeof(char));
	ptr->cheSerPat=(char*)malloc((strlen(ptr->fulScriPat)+strlen(cheSer)+10)*sizeof(char));
	sprintf(ptr->conFilPat, "%s%s", ptr->fulScriPat, conFil);
	printf("The path to the configuration file is %s\n.", ptr->conFilPat);
	sprintf(ptr->batFilPat, "%s%s", ptr->fulScriPat, batFil);
	printf("The path to the batch file is %s\n.", ptr->batFilPat);
	sprintf(ptr->cheSerPat, "%s%s", ptr->fulScriPat, cheSer);
	printf("The path to the check server is %s\n.", ptr->cheSerPat);

	/* Start the server in  a non-blocking mode */
	pid=(HANDLE)_spawnl(P_NOWAIT,  ptr->batFilPat,  ptr->batFilPat,
		ptr->fulScriPat, NULL);

	/* Create string for checking is up */
	sprintf(str, "%s%s", "python ", ptr->cheSerPat);
	retVal=system(str);

    /* Check if the server is up */
	while(retVal!=0){
	  retVal=system(str);
	  inc=inc+10;
#ifdef _MSC_VER
	  Sleep(10);
#endif
	}

	printf("The server is up after %f milli-seconds\n", inc);
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

	ptr->strParNam = (char*)malloc((nStrPar*500)*sizeof(char));
	ptr->strParVal = (char*)malloc((nStrPar*500)*sizeof(char));
	ptr->dblParNam = (char*)malloc((nDblPar*500)*sizeof(char));
	ptr->dblParVal = (char*)malloc((nDblPar*500)*sizeof(char));

	/* Join the strings */
	sprintf(ptr->strParNam, "%s", join_strings(strParNam, nStrPar));
	ptr->strParNam[strlen(ptr->strParNam)-1]=0;

	/* Join the strings */
	sprintf(ptr->strParVal, "%s", join_strings(strParVal, nStrPar));
	ptr->strParVal[strlen(ptr->strParVal)-1]=0;

	/* Join the strings */
	sprintf(ptr->dblParNam, "%s", join_strings(dblParNam, nDblPar));
	ptr->dblParNam[strlen(ptr->dblParNam)-1]=0;

	/* Convert the doubles values into doubles strings and 
	then convert the string into a single string */
	tmpDblParVal = (char**)malloc(nDblPar*sizeof(char*));
	for (i=0; i<nDblPar; i++){
		tmpDblParVal[i] = (char*)malloc(100*sizeof(char));
		sprintf(tmpDblParVal[i], "%.8f", dblParVal[i]);
	}

	/* Join the strings */
	sprintf(ptr->dblParVal, "%s", join_strings(tmpDblParVal, nDblPar));
	ptr->dblParVal[strlen(ptr->dblParVal)-1]=0;

	url_str=(char*)malloc((strlen(ptr->address)+
		strlen(ptr->port)+strlen(ptr->strParNam)+strlen(ptr->dblParNam)
		+strlen(ptr->strParVal)+strlen(ptr->dblParVal)+100)*sizeof(char));
	
	/* Write the string to initialize server */
	sprintf(url_str, "%s%s%s%s%s%s%s%s%s%s%s%s%s%s", "http://",
	ptr->address, ":", ptr->port, "/", "initialize", "/", 
	ptr->strParNam, ",", ptr->dblParNam, "&", 
	ptr->strParVal, ",", ptr->dblParVal);
	
	/* Initialize global session */
	curl_global_init(CURL_GLOBAL_ALL);

	/* init the curl session */
	ptr->curl_handle = curl_easy_init();

	/* specify URL to get */
	curl_easy_setopt(ptr->curl_handle, CURLOPT_URL, url_str);

	/* send all data to this function  */
	curl_easy_setopt(ptr->curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);

	/* we pass our 'chunk' struct to the callback function */
	curl_easy_setopt(ptr->curl_handle, CURLOPT_WRITEDATA, (void *)&chunk);

	/* send the values from the server */
	res = curl_easy_perform(ptr->curl_handle);

	/* check for errors */
	if(res != CURLE_OK) {
		fprintf(stderr, "curl_easy_perform() failed to initialize the server: %s\n",
			curl_easy_strerror(res));
		printf("curl_easy_perform() failed: %s\n",
			curl_easy_strerror(res));
		exit(1);
	}

	/* This might be ignored to avoid seg fault */
	/* This somehow causes the simulation to run*/
	/*for (i=0; i<nDblPar; i++){
		free(tmpDblParVal[i]);
	}
	
	free(tmpDblParVal);
	if (tmpScri!=NULL){
		free(tmpScri);
	}
	*/
	free(url_str);
	free(chunk.memory);
	ptr->ptr = NULL;
	ptr->isInitialized = 0;
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
* @param resWri the result flag
* @param ModelicaFormatError the pointer
* to the ModelicaFormatError
* @param memory a Server object
*/
void serverSimulatorVariables(
	double modTim,
	const size_t nDblWri,
	const char ** strWri,
	double * dblValWri,
	size_t nDblRea,
	const char ** strRea,
	double * dblValRea,
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
		chunk.memory = (char*)malloc(sizeof(char)*10000);  /* will be grown as needed by the realloc above */
		chunk.size = 0;    /* no data at this point */

		cMemory->inVal = (char*)malloc((nDblWri*500)*sizeof(char));
		if (cMemory->ptr==NULL){
			cMemory->inNam = (char*)malloc((nDblWri*500)*sizeof(char));
			cMemory->outNam = (char*)malloc((nDblRea*500)*sizeof(char));

			/* Join the strings */
			sprintf(cMemory->inNam, "%s", join_strings(strWri, nDblWri));
			cMemory->inNam[strlen(cMemory->inNam)-1]=0;

			/* Join the strings */
			sprintf(cMemory->outNam, "%s", join_strings(strRea, nDblRea));
			cMemory->outNam[strlen(cMemory->outNam)-1]=0;
		}

		/* Convert the doubles values into doubles strings and 
		   then convert the string into a single string */
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
			time_str, "&", cMemory->inNam, "&", 
			cMemory->inVal, "&", cMemory->outNam);

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
		/*
		for (i=0; i<nDblWri; i++){
			free(tmpInVal[i]);
		}
		free(tmpInVal);
		*/

		free(url_str);
		free(chunk.memory);
		free(cMemory->inVal);
		cMemory->isInitialized=1;
		memory = cMemory;
		cMemory->ptr=memory;
		return;
}

void freeServerMemory(void* object)
{
	if ( object != NULL ){
		char* url_str;
		CURLcode res;
		cPtr* p;

		struct MemoryStruct chunk;
				
		chunk.memory = (char*)malloc(sizeof(char)*10000);  /* will be grown as needed by the realloc above */
		chunk.size = 0;    /* no data at this point */

		p = (cPtr*) object;

		url_str=(char*)malloc((strlen(p->address)+
		strlen(p->port)+100)*sizeof(char));

		/* Write the string to shutdown the server */
		sprintf(url_str, "%s%s%s%s%s%s", "http://",
		p->address, ":", p->port, "/", "shutdown");

		/* specify URL to get */
		curl_easy_setopt(p->curl_handle, CURLOPT_URL, url_str);

		/* send all data to this function  */
		curl_easy_setopt(p->curl_handle, CURLOPT_WRITEFUNCTION, WriteMemoryCallback);

		/* we pass our 'chunk' struct to the callback function */
		curl_easy_setopt(p->curl_handle, CURLOPT_WRITEDATA, (void *)&chunk);

		/* get the values from the server */
		res = curl_easy_perform(p->curl_handle);

		/* check for errors */
		if(res != CURLE_OK) {
			fprintf(stderr, "curl_easy_perform() failed to shutdown the server: %s\n",
				curl_easy_strerror(res));
			printf("curl_easy_perform() failed: %s\n",
				curl_easy_strerror(res));
			exit(1);
		}
		printf("The address and the port shut down are %s and %s.\n", p->address, p->port);
		printf("Final response from the server is %s\n", chunk.memory);
		free(url_str);
		free(chunk.memory);
		curl_easy_cleanup(p->curl_handle);
		curl_global_cleanup();
		/*
		free(p->conFilPat);
		free(p->batFilPat);
		free( p->fulScriPat);
		free(p->inNam);
		free(p->outNam);
		free(p->strParNam);
		free(p->strParVal);
		free(p->dblParNam);
		free(p->dblParVal);
		free(p);
		*/
	}
}

