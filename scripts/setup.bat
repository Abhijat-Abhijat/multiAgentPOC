@echo off
REM Create virtual environment if not exists
if not exist "environment" (
    python -m venv environment
)

REM Activate virtual environment
call environment\Scripts\activate

REM Upgrade pip
python -m pip install --upgrade pip

REM Install requirements
pip install -r requirements.txt

echo.
echo Installation complete. To activate the environment, run:
echo call environment\Scripts\activate