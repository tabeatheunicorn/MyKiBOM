@ECHO OFF

Title Installing MiKTeX
ECHO =========================
miktexsetup --verbose --local-package-repository=C:\temp\miktex --package-set=complete download

ECHO Download completed
ECHO =========================
miktexsetup install

ECHO Installation completed
ECHO =========================
mpm --repository=ftp://ftp.tu-chemnitz.de/pub/tex/systems/win32/miktex/tm/packages/ --verbose --update-db
mpm --require=@required.txt --verbose
PAUSE