Set oShell = CreateObject ("Wscript.Shell") 
Dim strArgs
strArgs = "cmd /c MrSun.bat"
oShell.Run strArgs, 0, false