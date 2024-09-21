@echo off
setlocal

call .venv\Scripts\activate.bat

pip install -r requirements.txt
pip install -r requirements.txt

endlocal

pause