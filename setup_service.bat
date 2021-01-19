call nssm.exe install mis_errorData_dashboard "%cd%\run_server.bat"
rem call nssm.exe edit mis_errorData_dashboard
call nssm.exe set mis_errorData_dashboard AppStdout "%cd%\logs\mis_errorData_dashboard.log"
call nssm.exe set mis_errorData_dashboard AppStderr "%cd%\logs\mis_errorData_dashboard.log"
call sc start mis_errorData_dashboard