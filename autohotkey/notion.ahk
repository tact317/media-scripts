#Requires AutoHotkey v2.0
#SingleInstance Force
Persistent  ; ← 常駐を強制

; 起動確認（最初に1度だけ出る）※不要ならこの行2つは消してOK
TrayTip "AHK起動", "Notionの Ctrl+Shift+K を無効化中"

#HotIf WinActive("ahk_exe Notion.exe")
^+k::return   ; Ctrl+Shift+K を Notionで無効化
#HotIf
