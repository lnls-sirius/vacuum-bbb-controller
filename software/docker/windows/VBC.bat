@echo off

:: change the title of the cmd window
title Vacuum BBB Controller

:: change dir to where app is
cd C:\Users\%USERNAME%\Documents\ControleVBC\vacuum-bbb-controller\software\docker

:: enable CR (carriage return) character
setlocal enableextensions enabledelayedexpansion
for /f %%a in ('copy /Z "%~dpf0" nul') do set "CR=%%a"

:: print and check app condition
echo Checking app condition:
(docker version > NUL 2>&1) && (echo App is running^^! && echo Launching supervisory window... && docker-compose up -d && goto end) || goto loop

:: loop that prints message while docker is initialing
:loop
::--------------------------------------------
<nul set /p="App is starting.    !CR!"
timeout /t 1 /nobreak > NUL
<nul set /p="App is starting..   !CR!"
timeout /t 1 /nobreak > NUL
<nul set /p="App is starting...  !CR!"
timeout /t 1 /nobreak > NUL
<nul set /p="App is starting.... !CR!"
timeout /t 1 /nobreak > NUL
<nul set /p="App is starting.....!CR!"
timeout /t 1 /nobreak > NUL
::--------------------------------------------
:: run command "docker images"
:: if command succeeds, print "App is running!" and launch app
:: if not, run loop and check if docker daemon is up again
(docker version > NUL 2>&1) && (echo App is starting..... && echo App is running^^! && echo Launching supervisory window... && docker-compose up -d) || goto loop

:end