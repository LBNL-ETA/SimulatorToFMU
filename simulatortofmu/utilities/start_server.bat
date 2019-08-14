REM With FMU compiled with JModelica 2.1
REM C:\JModelica.org-2.4\setenv.bat && pip install -r %1requirements.txt && python.exe %1run_server.py %1
C:\JModelica.org-2.4\setenv.bat && cd %1 && cd ..\1 && python.exe run_server.py %1