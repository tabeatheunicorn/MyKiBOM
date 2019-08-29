ECHO OFF	

TITLE Uninstalling KiBOM with TeX

ECHO ===================================
::Finding Uninstall Path
for /f "tokens=3* delims= " %%O in ('reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KiBOMWithTeX" /v InstallLocation') do (
	set SkriptLocation=%%O %%P)
ECHO %SkriptLocation%

:: Path is choosen as the one where the installation folder is. Because Admin permissions are needed, the current Path is changed
set curpath=%~dp0

ECHO ===================================
ECHO Deleting KiBOM Scripts
del /q "%SkriptLocation%\LatexModule.*"
del /q "%SkriptLocation%\KiBOMWithTeX.*"
rmdir /q /s "C:\\Bilder\"

if not exist %SkriptLocation%\LatexModule.* (echo Deleted) else (echo Didn't work. Try as Admin)


ECHO ===================================

ECHO Deleting Registry Entry
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KiBOMWithTeX" 
IF %ERRORLEVEL% EQU 1 GOTO Ende

reg delete "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\KiBOMWithTeX" /f

:Ende
ECHO Uninstalled successfully

PAUSE