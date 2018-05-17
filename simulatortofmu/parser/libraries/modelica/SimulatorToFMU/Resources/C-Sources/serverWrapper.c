
/*
* This function is a Modelica wrapper
* function which invokes the C-function
* used to exchange variables with an
* external simulator.
*
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
* @param memory a Server object
*/
#include <ModelicaUtilities.h>

void modelicaToSimulator(
	double time,
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
	void* object)
{
	serverExchangeVariables(
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
		object);
}
