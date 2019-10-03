ECHO OFF

:: This CMD script makes sure that everything is setup fine to execute custom python kibom script based on latex and installs the files at the right place.

TITLE INSTALLING LATEX PYTHON KIBOM	
ECHO =========================

:: Path is choosen as the one where the installation folder is. Because Admin permissions are needed, the current Path is changed
set curpath=%~dp0

:: Checking if all python and other files needed during the process are in this folder
ECHO Checking if all Files needed are in this folder

if exist "%curpath%\KiBOMWithTeX_V1_3.py" ( 
	if exist "%curpath%\LatexModule.py" (
		echo All files found)
	)else (ECHO Not all Files found.)

ECHO =========================

ECHO Searching for KiCad Installation

:: Answer contains 3 values, all values separated with " "-> token nr 3 is the value we had a look for.
:: Version is stored in variable %version%
for /f "tokens=3 delims= " %%O in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\KiCad" /v DisplayVersion') do (set version=%%O)

for /f "tokens=3* delims= " %%O in ('reg query "HKEY_LOCAL_MACHINE\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\KiCad" /v InstallLocation') do (
set kicadLocation=%%O %%P)

ECHO %kicadLocation%

:: Currentyl tested with version 5.0.1_4
set getesteteVersionsNummer=5.0.1_4
set correct=0
if %version% EQU %getesteteVersionsNummer% (set correct=1
	echo Richtige Version gefunden.) else (echo !!!   Falsche KiCad Version %version% gefunden   !!!)

PAUSE
ECHO =========================

ECHO Searching for MiKTeX Installation

:: Test if Registry Keys are found
set correct=0

reg query "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\MiKTeX 2.9" 
IF %ERRORLEVEL% EQU 0 (set correct=1)

reg query "HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Uninstall\MiKTeX 2.9" 
IF %ERRORLEVEL% EQU 0 (set correct=1)

if %correct% EQU 1 (ECHO Found MiKTeX) else ECHO Not Found & set /p install="Zum Installieren y eingeben:" 

::if %install%==y Echo Will be installed & cmd /c "%curpath%test.cmd"

PAUSE
ECHO =========================

ECHO Putting Files in the right place


ECHO %curpath%
PAUSE

robocopy %curpath% "%kicadLocation%\bin\scripting\plugins" *.py  /NS /NC /NDL /NJH /NJS /NFL
robocopy %curpath% "%kicadLocation%\bin" UninstallKiBOMWithTeX.bat /NS /NC /NDL /NJH /NJS /NFL

if not exist "C:\\Bilder\" mkdir "C:\\Bilder\"
robocopy %curpath% "C:\\Bilder" AI_Stencil.png  /NS /NC /NDL /NJH /NJS /NFL
ECHO =========================

ECHO Checking if copying was successfull


if exist "%kicadLocation%\bin\scripting\plugins\LatexModule.py" (
	if exist "%kicadLocation%\bin\scripting\plugins\KiBOMWithTeX.py" (
	echo Files are in the right place)
	) else (echo Missing Files)

ECHO =========================

:: Adding information to registry
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KiBOMWithTeX" /v DisplayName /t REG_SZ /d "KiBOM with TeX"
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KiBOMWithTeX" /v DisplayVersion /t REG_SZ /d 1.3
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KiBOMWithTeX" /v InstallLocation /t REG_SZ /d "%kicadLocation%\bin\scripting\plugins"
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KiBOMWithTeX" /v NoModify /t REG_DWORD /d 1
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KiBOMWithTeX" /v Publisher /t REG_SZ /d "Tabea"
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KiBOMWithTeX" /v UninstallPath /t REG_SZ /d "%kicadLocation%\bin\UninstallKiBOMWithTeX.bat"
reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KiBOMWithTeX" /v UninstallString /t REG_SZ /d "%kicadLocation%\bin\UninstallKiBOMWithTeX.bat"

ECHO =========================
PAUSE
ECHO Performing Test

:: Testing with Python from KiCAD and board.xml File

"%kicadLocation%\bin\python.exe" "%kicadLocation%\bin\scripting\plugins/KiBOMWithTeX.py" "%curpath%\board.xml" "%curpath%\"

ECHO =========================
ECHO Test Results can be found in this folder.

PAUSE

ECHO =========================

ECHO Installation complete 

PAUSE
