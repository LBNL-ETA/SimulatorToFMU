
/*
 * Free and reset the server FMU.
 *
 * @param object Memory object.
 */
void freePythonMemory(void* object)
{
  if ( object != NULL ){
    cPtr* p = (cPtr*) object;
	free(p->patDir);
  free(p);
  }
}
