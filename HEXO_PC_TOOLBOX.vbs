
Option Explicit

Dim sh, fso, tempPath, htmlPath, file, i
Set fso = CreateObject("Scripting.FileSystemObject")
Set sh = CreateObject("WScript.Shell")

tempPath = sh.ExpandEnvironmentStrings("%TEMP%")
htmlPath = tempPath & "\NEXOS_Toolbox.hta"

Set file = fso.CreateTextFile(htmlPath, True)

file.WriteLine "<html><head><title> Universal Toolbox</title>"
file.WriteLine "<HTA:APPLICATION ID='Univercel toolbox' APPLICATIONNAME='univercel Toolbox' BORDER='thin' CAPTION='yes' SHOWINTASKBAR='yes' SCROLL='yes' />"
file.WriteLine "<style>"
file.WriteLine "body{background:#101827;color:white;font-family:Segoe UI;padding:20px}"
file.WriteLine "h1{color:#ff9d36}h2{color:#75baff}"
file.WriteLine ".panel{background:#1d2a3d;padding:15px;margin:12px 0;border-radius:10px}"
file.WriteLine "input{width:55%;padding:9px;background:#0c1421;color:white;border:1px solid #52647c;border-radius:5px}"
file.WriteLine "button{padding:9px 15px;background:#ff9d36;color:#101827;border:0;border-radius:5px;font-weight:bold;cursor:pointer}"
file.WriteLine ".slot{margin:9px 0}"
file.WriteLine "</style>"

file.WriteLine "<script language='VBScript'>"
file.WriteLine "Dim sh, wmi"
file.WriteLine "Set sh=CreateObject(""WScript.Shell"")"
file.WriteLine "Set wmi=GetObject(""winmgmts:\\.\root\cimv2"")"

file.WriteLine "Sub ShowHardware"
file.WriteLine " Dim x, item, s, total, free"
file.WriteLine " On Error Resume Next"
file.WriteLine " Set x=wmi.ExecQuery(""Select * from Win32_Processor"")"
file.WriteLine " For Each item In x"
file.WriteLine "  document.getElementById(""cpu"").innerHTML=item.Name & ""<br>Speed: "" & item.MaxClockSpeed & "" MHz"""
file.WriteLine " Next"
file.WriteLine " Set x=wmi.ExecQuery(""Select * from Win32_VideoController"")"
file.WriteLine " For Each item In x"
file.WriteLine "  document.getElementById(""gpu"").innerHTML=document.getElementById(""gpu"").innerHTML & item.Name & ""<br>"""
file.WriteLine " Next"
file.WriteLine " Set x=wmi.ExecQuery(""Select * from Win32_ComputerSystem"")"
file.WriteLine " For Each item In x"
file.WriteLine "  document.getElementById(""ram"").innerHTML=Round(item.TotalPhysicalMemory/1073741824,2) & "" GB"""
file.WriteLine " Next"
file.WriteLine " Set x=wmi.ExecQuery(""Select * from Win32_BaseBoard"")"
file.WriteLine " For Each item In x"
file.WriteLine "  document.getElementById(""board"").innerHTML=item.Manufacturer & "" - "" & item.Product"
file.WriteLine " Next"
file.WriteLine " Set x=wmi.ExecQuery(""Select * from Win32_LogicalDisk Where DriveType=3"")"
file.WriteLine " For Each item In x"
file.WriteLine "  If Not IsNull(item.Size) Then"
file.WriteLine "   s=s & item.DeviceID & "" | Total: "" & Round(item.Size/1073741824,2) & "" GB | Free: "" & Round(item.FreeSpace/1073741824,2) & "" GB<br>"""
file.WriteLine "  End If"
file.WriteLine " Next"
file.WriteLine " document.getElementById(""storage"").innerHTML=s"
file.WriteLine " document.getElementById(""pcname"").innerHTML=sh.ExpandEnvironmentStrings(""%COMPUTERNAME%"")"
file.WriteLine " document.getElementById(""windows"").innerHTML=sh.RegRead(""HKLM\SOFTWARE\Microsoft\Windows NT\CurrentVersion\ProductName"")"
file.WriteLine " document.getElementById(""arch"").innerHTML=sh.ExpandEnvironmentStrings(""%PROCESSOR_ARCHITECTURE%"")"
file.WriteLine " On Error GoTo 0"
file.WriteLine "End Sub"

file.WriteLine "Sub Window_OnLoad"
file.WriteLine " Dim i,p"
file.WriteLine " ShowHardware"
file.WriteLine " For i=1 To 10"
file.WriteLine "  On Error Resume Next"
file.WriteLine "  p=sh.RegRead(""HKCU\Software\NEXOS\Toolbox\App"" & i)"
file.WriteLine "  If Err.Number=0 Then document.getElementById(""app"" & i).value=p"
file.WriteLine "  Err.Clear"
file.WriteLine "  On Error GoTo 0"
file.WriteLine " Next"
file.WriteLine "End Sub"

file.WriteLine "Sub SavePath(n)"
file.WriteLine " On Error Resume Next"
file.WriteLine " sh.RegWrite ""HKCU\Software\NEXOS\Toolbox\App"" & n,document.getElementById(""app"" & n).value,""REG_SZ"""
file.WriteLine " On Error GoTo 0"
file.WriteLine "End Sub"

file.WriteLine "Sub OpenApp(n)"
file.WriteLine " Dim p"
file.WriteLine " p=Trim(document.getElementById(""app"" & n).value)"
file.WriteLine " If p="""" Then MsgBox ""Choose an app first."": Exit Sub"
file.WriteLine " SavePath n"
file.WriteLine " On Error Resume Next"
file.WriteLine " sh.Run Chr(34) & p & Chr(34),1,False"
file.WriteLine " If Err.Number<>0 Then MsgBox ""Could not open app. Check the path."",48,""NEXOS"""
file.WriteLine " On Error GoTo 0"
file.WriteLine "End Sub"

file.WriteLine "Sub ChooseApp(n)"
file.WriteLine " Dim d"
file.WriteLine " Set d=CreateObject(""UserAccounts.CommonDialog"")"
file.WriteLine " On Error Resume Next"
file.WriteLine " d.Filter=""Programs and files|*.exe;*.bat;*.cmd;*.vbs;*.lnk|All files|*.*"""
file.WriteLine " d.FilterIndex=1"
file.WriteLine " If d.ShowOpen Then"
file.WriteLine "  document.getElementById(""app"" & n).value=d.FileName"
file.WriteLine "  SavePath n"
file.WriteLine " End If"
file.WriteLine " On Error GoTo 0"
file.WriteLine "End Sub"
file.WriteLine "</script></head><body onload='ShowHardware'>"

file.WriteLine "<h1>NEXOS TOOLBOX</h1>"
file.WriteLine "<p>Universal PC hardware and app launcher</p>"
file.WriteLine "<div class='panel'><h2>PC INFORMATION</h2>"
file.WriteLine "<b>CPU</b><p id='cpu'>Loading...</p>"
file.WriteLine "<b>GPU</b><p id='gpu'>Loading...</p>"
file.WriteLine "<b>RAM</b><p id='ram'>Loading...</p>"
file.WriteLine "<b>STORAGE</b><p id='storage'>Loading...</p>"
file.WriteLine "<b>MOTHERBOARD</b><p id='board'>Loading...</p>"
file.WriteLine "<b>PC NAME</b><p id='pcname'>Loading...</p>"
file.WriteLine "<b>WINDOWS</b><p id='windows'>Loading...</p>"
file.WriteLine "<b>ARCHITECTURE</b><p id='arch'>Loading...</p>"
file.WriteLine "<button onclick='ShowHardware'>REFRESH INFO</button></div>"

file.WriteLine "<div class='panel'><h2>UNIVERSAL APP LAUNCHER</h2>"
file.WriteLine "<p>Choose apps and save their paths automatically.</p>"

For i=1 To 10
 file.WriteLine "<div class='slot'><b>APP " & i & "</b><br>"
 file.WriteLine "<input id='app" & i & "' type='text' onchange='SavePath " & i & "' placeholder='App path...'> "
 file.WriteLine "<button onclick='ChooseApp " & i & "'>BROWSE</button> "
 file.WriteLine "<button onclick='OpenApp " & i & "'>OPEN</button></div>"
Next

file.WriteLine "</div><p> Universal Toolbox</p></body></html>"
file.Close

sh.Run "mshta.exe " & Chr(34) & htmlPath & Chr(34),1,False
