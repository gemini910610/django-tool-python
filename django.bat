@echo off
setlocal enabledelayedexpansion
set mode=%1%
set project=%2%
set app=%3%
set commit=%4%
if "%mode%" == "" (
@echo What do you want to do ?
@echo 1. make
@echo 2. upload
@echo 3. runserver
set /p mode=^>^> 
)
if %mode% equ 1 (
python djangomaker.py %project% %app%
) else if %mode% equ 2 (
python djangoupload.py %project% %app% %commit%
) else if %mode% equ 3 (
if "%project%" == "" (
set /p project=Project: 
)
cls
python !project!/manage.py runserver
pause
) else (
@echo [error] input error
@echo.
pause
)