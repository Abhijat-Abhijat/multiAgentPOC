@echo off

REM Activate virtual environment
call environment/Scripts/activate.bat

REM Navigate to project directory
cd multiganet_web

REM Run Uvicorn server
uvicorn main:app --reload

pause
