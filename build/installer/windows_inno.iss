; Inno Setup Script for Astro Sahayogi (Windows)
[Setup]
AppName=Astro Sahayogi
AppVersion=1.0.0
AppPublisher=AstroSahayogi
DefaultDirName={autopf}\AstroSahayogi
DefaultGroupName=Astro Sahayogi
OutputDir=..\dist\installer
OutputBaseFilename=AstroSahayogi_Setup_v1.0.0
Compression=lzma2
SolidCompression=yes
; Optional: add ui\theme\assets\icon.ico and uncomment next line for a custom installer icon
; SetupIconFile=..\..\ui\theme\assets\icon.ico

[Files]
Source: "..\..\dist\main.exe"; DestDir: "{app}"; DestName: "AstroSahayogi.exe"; Flags: ignoreversion

[Icons]
Name: "{group}\Astro Sahayogi"; Filename: "{app}\AstroSahayogi.exe"
Name: "{commondesktop}\Astro Sahayogi"; Filename: "{app}\AstroSahayogi.exe"

[Run]
Filename: "{app}\AstroSahayogi.exe"; Description: "Launch Astro Sahayogi"; Flags: nowait postinstall skipifsilent
