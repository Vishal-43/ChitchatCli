@echo off
REM Welcome to cool project made with love by legends

echo welcome to chitchat by legend
echo what do you want to do?
echo 1. host a server
echo 2. join a server
echo 3. exit
set /p choice=Enter your choice (1-3):
if "%choice%"=="1" goto host
if "%choice%"=="2" goto join
if "%choice%"=="3" goto exit
echo Invalid choice. Please try again.
goto exit
:host
python start.py
REM Add commands to host a server here
goto exit
:join
echo Joining a server...
python start2.py
REM Add commands to join a server here
goto exit
:exit
echo Exiting...


pause