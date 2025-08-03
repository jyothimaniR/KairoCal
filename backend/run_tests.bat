@echo off
REM backend/run_tests.bat
REM Windows batch file to run BERT tests with proper Python path

echo Setting up Python path for KairoCal backend...
set PYTHONPATH=%cd%
echo PYTHONPATH set to: %PYTHONPATH%

echo.
echo Running BERT implementation tests...
python app/scripts/test_bert_implementation.py

pause
