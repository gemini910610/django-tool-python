@echo off
setlocal enabledelayedexpansion
set mode=%1%
set project=%2%
set app=%3%
set commit=%4%
if "%mode%" == "" (
@echo What do you want to do ?
@echo 1. make
@echo 2. upload^(heroku^)
@echo 3. upload^(git^)
@echo 4. runserver
@echo 5. migrate
set /p mode=^>^> 
)
if %mode% equ 1 (
python djangomaker.py %project% %app%
) else if %mode% equ 2 (
python djangoupload.py %project% %app% %commit%
) else if %mode% equ 3 (
python djangouploadgit.py %project% %commit%
) else if %mode% equ 4 (
if "%project%" == "" (
set /p project=Project: 
)
start cmd /k "python !project!/manage.py runserver"
start http://127.0.0.1:8000/%app%
) else if %mode% equ 5 (
if "%project%" == "" (
set /p project=Project: 
)
python !project!/manage.py makemigrations
python !project!/manage.py migrate
@echo.
pause
) else (
@echo [error] input error
@echo.
pause
)