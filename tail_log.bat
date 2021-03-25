
@Echo off
:: Check WMIC is available
WMIC.EXE Alias /? >NUL 2>&1 || GOTO s_error

:: Use WMIC to retrieve date and time
FOR /F "skip=1 tokens=1-6" %%G IN ('WMIC Path Win32_LocalTime Get Day^,Hour^,Minute^,Month^,Second^,Year /Format:table') DO (
   IF "%%~L"=="" goto s_done
      Set _yyyy=%%L
      Set _mm=00%%J

)
:s_done

:: Pad digits with leading zeros
      Set _mm=%_mm:~-2%
      Set _dd=%_dd:~-2%
      Set _hour=%_hour:~-2%
      Set _minute=%_minute:~-2%

:: Display the date/time in ISO 8601 format:

:: The command we are trying to run: powershell -command Get-Content %0\..\Log\2021_03_connection_monitor.txt -Wait
set FILE_PATH= %0\..\Log\
set FILE_NAME=_connection_monitor.txt
Set _isodate=%FILE_PATH%%_yyyy%_%_mm%%FILE_NAME%

Echo %_isodate%
set WAIT=-Wait

set COMMAND= Get-Content %_isodate% %WAIT%
powershell -command %COMMAND%

