call nssm.exe install mis_data_dashboard "%cd%\run_server.bat"
rem call nssm.exe edit mis_data_dashboard
call nssm.exe set mis_data_dashboard AppStdout "%cd%\logs\mis_data_dashboard.log"
call nssm.exe set mis_data_dashboard AppStderr "%cd%\logs\mis_data_dashboard.log"
call sc start mis_data_dashboard