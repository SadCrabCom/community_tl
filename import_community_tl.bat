@echo This script will convert lines.json into game translations refreshing its current state.
@if "%~1" == "--silent" goto silent
@echo Press any key to continue or close the window to prevent the script from running!
@pause

:silent
@call convert_and_call.bat game compile
@call convert_and_call.bat game import_community_tl
@if "%~1" neq "--silent" pause
