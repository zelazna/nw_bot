OutFile "NWBotInstaller.exe"
InstallDir "$PROGRAMFILES\NWBot"

Section
  SetOutPath "$INSTDIR"
  File "dist\nwbot.exe"
  CreateShortcut "$DESKTOP\NWBot.lnk" "$INSTDIR\nwbot.exe"
SectionEnd
