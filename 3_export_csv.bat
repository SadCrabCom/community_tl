@echo This script will regenerate export folder based on current state of import. Press any key to continue or close the window to prevent the script from running!
@pause
@call convert_and_call.bat game compile
@call convert_and_call.bat game export_csv
@pause
