/* ENABLE FOR DEBUGGING (VISUAL STUDIO)*/
/* #define _CRTDBG_MAP_ALLOC*/
/* #include <stdlib.h>*/
/* #include <crtdbg.h>*/
#include "testProgram.h"

void ModelicaFormatError(const char* string, const char* fmt, const char* val){
	fprintf(stderr, string, fmt, val);
	fprintf(stderr, "\n");
	exit(1);
}

int main(int nArgs, char ** args){

	/* Parameters for testing simulator interface*/
	const char * moduleName="testSimulator";
	const char * functionName="r1_r1PassPythonObject";
	const char * configFileName="config.csv";
	double time=0.0;

	size_t nDblWri=1;
	double dblValWri[]={15.0};
	const char *strWri[]={"u"};

	size_t nDblRea=1;
	double dblValRea[1];
	const char *strRea[]={"y"};

	size_t nDblParWri=0;
	const char * strParWri[]={""};
	double dblValParWri[]={0};
	int resWri=1;

	int i;
        pythonPtr* ptr = malloc(sizeof(pythonPtr));
        /* Set ptr to null as pythonExchangeValuesNoModelica is checking for this */
        ptr->ptr = NULL;
        ptr->isInitialized = 0;
	
	/*_CrtDumpMemoryLeaks(); //DEBUGGING*/
	for(i=0; i < 10; i++){
		printf("Calling with i for simulator = %d.\n", i);
		pythonExchangeVariables(moduleName,
			functionName, 
			configFileName, 
			time,
			nDblWri, 
			strWri, 
			dblValWri, 
			nDblRea, 
			strRea,
			dblValRea, 
			nDblParWri, 
			strParWri, 
			dblValParWri, 
			resWri,
			ModelicaFormatError,
			ptr,
			1);
	}

	return 0;
}

