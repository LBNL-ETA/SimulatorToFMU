/* ENABLE FOR DEBUGGING (VISUAL STUDIO)*/
/* #define _CRTDBG_MAP_ALLOC*/
/* #include <stdlib.h>*/
/* #include <crtdbg.h>*/
#include "pythonInterpreter.h"
#define MAX_PATHNAME_LEN 2048
#define STR_FLAG 1
#define DBL_FLAG 0
#if PY_MAJOR_VERSION >= 3
#define IS_PY3K
#endif

/* Must define Py_TYPE for Python 2.5 or older */
#ifndef PyInt_Check
# define PyInt_Check PyLong_Check
#endif

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

/* Create the structure and initialize its pointer to NULL. */
void* initPythonMemory(char* pytScri)
{
  pythonPtr* ptr = malloc(sizeof(pythonPtr));
#ifdef _MSC_VER
  char pathDir[MAX_PATHNAME_LEN];
  char base [MAX_PATHNAME_LEN];
  int retVal;
  char ext [40];
#elif __unix__
  char* basec;
  char* pathDir;
#endif


  /* Split the path to extract the directory name*/
#ifdef _MSC_VER
  retVal=_splitpath_s(str_replace(pytScri, "\\", "/"), base, sizeof(base),
  pathDir, sizeof(pathDir), NULL, 0, NULL, 0);
  if(retVal!=0){
	  fprintf(stderr, "Python script %s could not be splitted. "
		  "The error code is %d\n", pytScri, retVal);
  }
#elif __unix__
  basec=strdup(pytScri);
  pathDir=dirname(basec);
#endif

  /* Set ptr to null as pythonExchangeValuesNoModelica is checking for this */
  ptr->ptr = NULL;
  ptr->isInitialized = 0;
  ptr->pModule = NULL;
  ptr->pFunc = NULL;
#ifdef _MSC_VER
  ptr->pathDir = (char *)malloc((strlen(pathDir) + strlen(base) + 50)*sizeof(char));
#elif __unix__
  ptr->pathDir = (char *)malloc((strlen(pathDir) + 50)*sizeof(char));
#endif
  if (!Py_IsInitialized())
	Py_Initialize();
  	PyRun_SimpleString("import sys");
  /* Append the path to the Python script to the Python search path*/
#ifdef _MSC_VER
	sprintf(ptr->pathDir, "%s%s%s%s%s%s", "sys.path.append(", "\"", pathDir, base, "\"", ")");
#elif __unix__
        sprintf(ptr->pathDir, "%s%s%s%s%s", "sys.path.append(", "\"", pathDir, "\"", ")");
#endif
	printf ("The path to the Python script directory is %s\n", ptr->pathDir);
	PyRun_SimpleString(ptr->pathDir);
  return (void*) ptr;
}

static Py_ssize_t iArg = 0;

/*
 * This function creates list of
 * arguments for the Python function.
 *
 * @param typ the type of variable
 * (1 for strings, 0 for doubles)
 * @param nStrs the number of string variables
 * @param nDbls the number of double variables
 * @param strs the string variables\
 * @param dbls the double variables
 * @param ptrMemory->pModule the module name
 * @param ptrMemory->pFunc the function name
 * @param pArgs the number of arguments
 * @param ModelicaFormatError the pointer
 * to the ModelicaFormatError
 */
void createPythonArgumentLists(int typ,
	const size_t nStrs,
	const size_t nDbls,
	const char ** strs,
	double * dbls,
	PyObject *pModule,
	PyObject *pFunc,
	PyObject *pArgs,
	void (*ModelicaFormatError)
	(const char *string,...)){
		Py_ssize_t i;
		PyObject *pArgsDbl;
		PyObject *pArgsStr;
		PyObject *pValue;

		if(typ==DBL_FLAG){
			pArgsDbl = PyList_New(nDbls);
			for (i = 0; i < nDbls; ++i) {
				/* Convert argument to a python float*/
				pValue = PyFloat_FromDouble(dbls[i]);
				if (!pValue) {
					/* Failed to convert argument.*/
					Py_DECREF(pArgsDbl);
					Py_DECREF(pModule);
					/* According to the Modelica specification,*/
					/* the function ModelicaError never returns to the calling function.*/
					(*ModelicaFormatError)("Cannot convert double argument number %i to Python format.", i);
				}
				/* pValue reference stolen here*/
				PyList_SetItem(pArgsDbl, i, pValue);
			}
			/* If there is only a scalar double, then don't build a list.*/
			/* Just put the scalar value into the list of arguments*/
			if ( nDbls == 1)
				PyTuple_SetItem(pArgs, iArg, PyList_GetItem(pArgsDbl, (Py_ssize_t)0));
			else
				PyTuple_SetItem(pArgs, iArg, pArgsDbl);
			iArg++;
		}
		else if (typ==STR_FLAG){
			pArgsStr = PyList_New(nStrs);

			for (i = 0; i < nStrs; ++i) {
				/* Convert argument to a python float*/
				/* PyUnicode in Python27 is PyString in Python34*/
				pValue = PyUnicode_FromString(strs[i]);

				if (!pValue) {
					/* Failed to convert argument.*/
					Py_DECREF(pArgsStr);
					Py_DECREF(pModule);
					/* According to the Modelica specification,*/
					/* the function ModelicaError never returns to the calling function.*/
					(*ModelicaFormatError)("Cannot convert string argument number %i to Python format.", i);
				}
				/* pValue reference stolen here*/
				PyList_SetItem(pArgsStr, i, pValue);
			}
			/* If there is only a scalar string, then don't build a list.*/
			/* Just put the scalar value into the list of arguments.*/
			if ( nStrs == 1)
				PyTuple_SetItem(pArgs, iArg, PyList_GetItem(pArgsStr, (Py_ssize_t)0));
			else
				PyTuple_SetItem(pArgs, iArg, pArgsStr);
			iArg++;
		}
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

	PyObject *pName;
	PyObject *pValue;
	PyObject *pArgs;

	Py_ssize_t pIndVal;
	PyObject *pItemDbl;
  	PyObject* obj;

	char* arg="";
	Py_ssize_t nStrWri = 0;
	Py_ssize_t nStrRea = 0;
	Py_ssize_t nStrParWri = 0;

	/* The number of arguments starts*/
	/* at 3 since we always have the */
	/* configuration file, the model time, */
	/* a flag to write results.*/
	Py_ssize_t nArg = 3;
	Py_ssize_t iRet = 0;
	Py_ssize_t nRet = 0;
  	pythonPtr* ptrMemory = (pythonPtr*)memory;

	const char *confFilNam [] = {configFileName};

	/*//////////////////////////////////////////////////////////////////////////*/
	/* Initialize Python interpreter*/
	/*_CrtDumpMemoryLeaks(); //DEBUGGING*/
        if (!Py_IsInitialized())
      	    Py_Initialize();
	/* Set the entries for sys.argv.*/
	/* This is required if a script uses sys.argv, such as bacpypes.*/
	/* See also http://stackoverflow.com/questions/19381441/python-modelica-connection-fails-due-to-import-error*/
	PySys_SetArgv(0, &arg);

	/*//////////////////////////////////////////////////////////////////////////*/
	/* Load Python module*/

        if (!ptrMemory->isInitialized) {
          /*pName = PyString_FromString(moduleName);*/
          pName = PyUnicode_FromString(moduleName);
          if (!pName) {
            (*ModelicaFormatError)("Failed to convert moduleName '%s' to Python object.\n", moduleName);
          }
	ptrMemory->pModule = PyImport_Import(pName);
	/* Decrement the reference counter */
	/* causes sometimes a segmentation fault Py_DECREF(pName);*/
	/* when exported as an FMU and run with PyFMI*/
	/*Py_DECREF(pName);*/
	if (!ptrMemory->pModule) {
		/*    PyErr_Print();*/
		PyObject *pValue, *pType, *pTraceBack;
		PyErr_Fetch(&pType, &pValue, &pTraceBack);
		if (pType != NULL)
			Py_DECREF(pType);
		if (pTraceBack != NULL)
			Py_DECREF(pTraceBack);
		/* Py_Finalize(); // removed, see note at other Py_Finalize() statement*/
		(*ModelicaFormatError)("Failed to load \"%s\".\n\
							   This may occur if you did not set the PYTHONPATH environment variable\n\
							   or if the Python module contains a syntax error.\n\
							   The error message is \"%s\"",
							   moduleName,
							   PyBytes_AsString(PyObject_Repr(pValue)));
	}

	/*//////////////////////////////////////////////////////////////////////////*/
	/* Python module is successfully loaded.*/
	/* Load function*/
	ptrMemory->pFunc = PyObject_GetAttrString(ptrMemory->pModule, functionName);
	/* ptrMemory->pFunc is a new reference */

	if (!(ptrMemory->pFunc && PyCallable_Check(ptrMemory->pFunc))){
		if (PyErr_Occurred())
			PyErr_Print();
		/* Py_Finalize(); // removed, see note at other Py_Finalize() statement*/
		(*ModelicaFormatError)(
			"Cannot find function \"%s\".\nMake sure PYTHONPATH contains the path of the module that contains this function.\n",
			functionName);
	}
       ptrMemory->isInitialized = 1;
     }

	/*//////////////////////////////////////////////////////////////////////////*/
	/* The function is loaded.*/
	/*//////////////////////////////////////////////////////////////////////////*/

	/* Convert the arguments*/
	/* a) Convert the input file name*/
	/* Create arguments for the python function*/
	if (nDblWri > 0){
		/* Increase the number of arguments to 2*/
		/* One is for the vector of input names*/
		/* to be sent to the Simulator FMU, the second one is*/
		/* for the vector of input values to be sent*/
		/* to the Simulator FMU.*/
		nStrWri = nDblWri;
		nArg = nArg + 2;
	}
	if (nDblRea > 0){
		/* Increase the number of argument to 1*/
		/* This is for the vector of output names.*/
		nStrRea = nDblRea;
		nArg++;
	}
	if (nDblParWri > 0){
		/* Increase the number of arguments to 2*/
		/* One is for the vector of strings parameters*/
		/* to be sent to the Simulator FMU, the second one is */
		/* for the vector of parameter values to be sent*/
		/* to the Simulator FMU.*/
		nStrParWri = nDblParWri;
		nArg = nArg + 2;
	}
        if (passPythonObject > 0)
                nArg++;
	if (nArg > 0)
		pArgs = PyTuple_New(nArg);
	else
		pArgs = NULL;

	/* Convert the arguments*/
	/* a) Convert the configuration file name*/
	createPythonArgumentLists(STR_FLAG, 1,
		0, confFilNam, NULL, ptrMemory->pModule,
		ptrMemory->pFunc, pArgs, *ModelicaFormatError
		);

	/* b) Convert double[]*/
        /*
	createPythonArgumentLists(DBL_FLAG, 0, 1,
		NULL, modTim, ptrMemory->pModule, ptrMemory->pFunc,
		pArgs, *ModelicaFormatError
		);
         */

	 /* b) Convert resWri*/
         pValue = PyFloat_FromDouble(modTim);
	 if (!pValue) {
		  /* Failed to convert argument.*/
		  Py_DECREF(ptrMemory->pModule);
		  /* According to the Modelica specification,*/
		  /* the function ModelicaError never returns to the calling function.*/
		  (*ModelicaFormatError)("Cannot convert the model time %f to Python format.", modTim);
		}
         PyTuple_SetItem(pArgs, iArg, pValue);
	 iArg++;

	/* c) Convert char **, an array of character arrays*/
	if ( nStrWri > 0 ){
		createPythonArgumentLists(STR_FLAG, nStrWri,
			0, strWri, NULL, ptrMemory->pModule,
			ptrMemory->pFunc, pArgs, *ModelicaFormatError
			);
	}

	/* d) Convert double[]*/
	if ( nDblWri > 0 ){
		createPythonArgumentLists(DBL_FLAG, 0,
			nDblWri, NULL, dblValWri, ptrMemory->pModule,
			ptrMemory->pFunc, pArgs, *ModelicaFormatError
			);
	}

	/* e) Convert char **, an array of character arrays*/
	if ( nStrRea > 0 ){
		createPythonArgumentLists(STR_FLAG,
			nStrRea, 0, strRea, NULL, ptrMemory->pModule,
			ptrMemory->pFunc, pArgs, *ModelicaFormatError
			);
	}

	/* f) Convert char **, an array of character arrays*/
	if (nStrParWri > 0){
		createPythonArgumentLists(STR_FLAG,
			nStrParWri, 0, strParWri, NULL,
			ptrMemory->pModule, ptrMemory->pFunc, pArgs,
			*ModelicaFormatError
			);
	}

	/* Convert the arguments*/
	/* g) Convert double[]*/
	if (nDblParWri > 0){
		createPythonArgumentLists(DBL_FLAG, 0,
			nDblParWri, NULL, dblValParWri,
			ptrMemory->pModule, ptrMemory->pFunc, pArgs,
			*ModelicaFormatError
			);
	}

	/* Convert the arguments*/
	/* h) Convert double[]*/
	/*createPythonArgumentLists(DBL_FLAG, 0,
		1, NULL, resWri, ptrMemory->pModule, ptrMemory->pFunc,
		pArgs, *ModelicaFormatError
		);
         */

	 /* h) Convert resWri*/
         pValue = PyLong_FromLong((long)resWri);
	 if (!pValue) {
		  /* Failed to convert argument.*/
		  Py_DECREF(ptrMemory->pModule);
		  /* According to the Modelica specification,*/
		  /* the function ModelicaError never returns to the calling function.*/
		  (*ModelicaFormatError)("Cannot convert the flag for saving results) %d to Python format.", resWri);
		}
         PyTuple_SetItem(pArgs, iArg, pValue);
	 iArg++;

	 /* i) Convert object*/
	 if ( passPythonObject > 0 ){
	   /* Put the memory into the argument list.*/
	   /* In the first call, put Py_None int obj, but in subsequent calls, use ptr. */
		obj = (ptrMemory->ptr == NULL) ? Py_None : ptrMemory->ptr;
	   	PyTuple_SetItem(pArgs, iArg, obj);
	   	iArg++;
	 }

	/*//////////////////////////////////////////////////////////////////////////*/
	/*//////////////////////////////////////////////////////////////////////////*/
	/* Call the Python function*/

	pValue = PyObject_CallObject(ptrMemory->pFunc, pArgs);

	/*//////////////////////////////////////////////////////////////////////////*/
	/* Decrement the reference counter when pArgs != NULL*/
	/* causes sometimes a segmentation fault Py_DECREF(pArgs);*/
	/* when exported as an FMU and run with PyFMI*/

	/*if (pArgs != NULL)*/
	/*  Py_DECREF(pArgs);*/

	/*//////////////////////////////////////////////////////////////////////////*/
	/* Check whether the call to the Python function failed.*/
	if (pValue == NULL) {

		/*    PyErr_Print();*/
		PyObject *pValue, *pType, *pTraceBack;
		PyErr_Fetch(&pType, &pValue, &pTraceBack);
		if (pType != NULL)
			Py_DECREF(pType);
		if (pTraceBack != NULL)
			Py_DECREF(pTraceBack);
		Py_DECREF(ptrMemory->pFunc);
		Py_DECREF(ptrMemory->pModule);
		/* Py_Finalize(); // removed, see note at other Py_Finalize() statement*/
		(*ModelicaFormatError)("Call to Python function \"%s\" failed.\n \
							   This is often due to an error in the Python script,\n \
							   or because the list of arguments of the Python function is incorrect.\n \
							   Check the module \"%s\".\n \
							   The error message is \"%s\"",
							   functionName, moduleName,
							   PyBytes_AsString(PyObject_Repr(pValue)));
	}

	/*//////////////////////////////////////////////////////////////////////////*/
	/* Set up the variables that indicate the return data types of the function*/
	if ( nDblRea > 0)
		nRet++;
	if (passPythonObject)
	    	nRet++;
	/* Check whether the function must returns some values*/
	if (nRet > 0){
		/*//////////////////////////////////////////////////////////////////////////*/
		/* The function returned some arguments.*/
		/* If there are multiple return values, then it must be a list*/
		if (nRet > 1){
			/* Check whether it is a list*/
			if (!PyList_Check(pValue)){
				(*ModelicaFormatError)("Python function \"%s\" does not return a list.\n\
									   The returned object is \"%s\"",
									   functionName, PyBytes_AsString(PyObject_Repr(pValue)));
			}
		}
		/* Check whether the list has the right number of arguments.*/
		/* If nRet==2, then it must be a list with two values. If nRet > 2, it may*/
		/* be a list with three values, or a two lists, one with one and one with two values.*/
		/* Hence, we only check for nRet==2.*/
		if ( nRet == 2){
			if ( nRet != PyList_Size(pValue) ){
				(*ModelicaFormatError)("Python function \"%s\", returns a list with %i elements,\n \
									   but expected two elements.\n\
									   The returned object is \"%s\"",
									   functionName,
									   PyList_Size(pValue),
									   PyBytes_AsString(PyObject_Repr(pValue)));
			}
		}
		/*//////////////////////////////////////////////////////////////////////////
		*/
		/* Parse double values, if we have some
		*/
		if (nDblRea > 0){
			/* Check if the function only returns double values
			*/
			if (nRet == 1)
				pItemDbl = pValue;
			else{
				pItemDbl = PyList_GetItem(pValue, iRet);
				iRet++;
			}
			/* Check the number of return arguments
			*/
			if (nDblRea > 1 && nDblRea != PyList_Size(pItemDbl))
				(*ModelicaFormatError)("For Python function \"%s\", Modelica declares that Python returns %i doubles,\
									   but Python returned %i values.\n\
									   The returned object is \"%s\"",
									   functionName, nDblRea, PyList_Size(pItemDbl),
									   PyBytes_AsString(PyObject_Repr(pValue)));

			/* The number of arguments is correct. Retrieve them and parse them.
			*/
			/* If nDblRea == 1, then it is a scalar, else it is a list
			*/
			if (nDblRea == 1){
				/* Check whether it is a float or an integer.
				*/
				/* (For integers, PyFloat_Check(p) returns false, hence we also call PyLong_Check(p) and PyInt_Check(pItemDbl)))
				*/
				if (PyFloat_Check(pItemDbl) || PyLong_Check(pItemDbl) || PyInt_Check(pItemDbl))
					dblValRea[0] = PyFloat_AsDouble(pItemDbl);
				else
					(*ModelicaFormatError)("Python function \"%s\" returns an invalid object for a scalar double value.\n\
										   There should only be one double value returned.\n\
										   The returned object is \"%s\".",
										   functionName, PyBytes_AsString(PyObject_Repr(pValue)));
			}
			else{ /* We have nDblRea > 1, iterate through the list
				  */
				for (pIndVal = 0; pIndVal < PyList_Size(pItemDbl); ++pIndVal){
					PyObject *p = PyList_GetItem(pItemDbl, pIndVal);
					/* Check whether it is a float or an integer.
					*/
					/* (For integers, PyFloat_Check(p) returns false, hence we also call PyLong_Check(p) and PyInt_Check(pItemDbl)))
					*/
					if (PyFloat_Check(p) || PyLong_Check(p) || PyInt_Check(p))
						dblValRea[pIndVal] = PyFloat_AsDouble(p);
					else
						(*ModelicaFormatError)("Python function \"%s\" returns an invalid object for a scalar double value.\n\
											   The returned object is \"%s\".",
											   functionName, PyBytes_AsString(PyObject_Repr(pValue)));
				} /* for(...)
				  */
			}
		}/* nDblRea > 0
		 */
		else{
			/* Modelica has no arrays with zero lenght. Hence, dblValRea has size 1 if nDblRea = 0.
			*/
			/* Assign a zero value to this element.
			*/
			dblValRea[0] = 0;
		}
    		/*//////////////////////////////////////////////////////////////////////////*/
    		/* Parse the memory to the Python object*/
    		if (passPythonObject > 0){
      			ptrMemory->ptr = (void*)PyList_GetItem(pValue, iRet);
     			 iRet++;
    }

	} /* end of if (nRet > 0)*/

	/*//////////////////////////////////////////////////////////////////////////*/
	/* Decrement the reference counters*/
	/* causes sometimes a segmentation fault    Py_DECREF(pValue);*/
	/* causes sometimes a segmentation fault    Py_DECREF(ptrMemory->pFunc);*/
	/* causes sometimes a segmentation fault    Py_DECREF(ptrMemory->pModule);*/
	/* Undo all initializations*/
	/* We uncommented Py_Finalize() because it caused a segmentation fault on Ubuntu 12.04 32 bit.*/
	/* The segmentation fault was randomly produced by the statement, and often observed when running*/
	/* simulateModel("the SimulatorToFMU.Utilities.IO.Python27.Functions.Examples.TestPythonInterface");*/
	/**/
	/* See also the discussion at*/
	/* http://stackoverflow.com/questions/7676314/py-initialize-py-finalize-not-working-twice-with-numpy*/
	/**/
	iArg = 0;
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
    pythonPtr* p = (pythonPtr*) object;
	free(p->pathDir);
    free(p);
  }
}
