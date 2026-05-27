@echo off
setlocal

cd /d "%~dp0"
set URL=http://127.0.0.1:8765

echo YomiEpub Studio
echo ================
echo This window starts the local converter web page.
echo First launch may take a few minutes while dependencies are installed.
echo.

where py >nul 2>nul
if %errorlevel%==0 (
  set PYTHON=py -3
) else (
  set PYTHON=python
)

if not exist ".venv" (
  echo Creating local Python environment...
  %PYTHON% -m venv .venv
  if errorlevel 1 goto python_error
)

echo Installing or updating YomiEpub Studio locally...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto install_error
".venv\Scripts\python.exe" -m pip install --upgrade "%cd%"
if errorlevel 1 goto install_error

echo.
echo Starting local web page:
echo %URL%
echo.
echo Keep this window open while using YomiEpub Studio.
echo Press Ctrl+C here to stop the server.
echo.

start "" "%URL%"
".venv\Scripts\jp-ebook-web.exe"
pause
exit /b 0

:python_error
echo.
echo Python 3 is required. Install it from https://www.python.org/downloads/ and run this file again.
pause
exit /b 1

:install_error
echo.
echo Install failed. Check the error above, then run this file again.
pause
exit /b 1
