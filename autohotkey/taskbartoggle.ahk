; タスクバー表示/非表示切り替えスクリプト
; Ctrl+Shift+A でタスクバーの表示/非表示を切り替え

; 初期状態（タスクバーが表示されているかどうか）
TaskbarVisible := true

^+a::  ; Ctrl+Shift+A のホットキー
{
    if (TaskbarVisible) {
        ; タスクバーを隠す
        WinHide, ahk_class Shell_TrayWnd
        WinHide, ahk_class Shell_SecondaryTrayWnd  ; マルチモニター用
        TaskbarVisible := false
        TrayTip, タスクバー, 非表示にしました (Ctrl+Shift+A で表示), 2, 1
    } else {
        ; タスクバーを表示
        WinShow, ahk_class Shell_TrayWnd
        WinShow, ahk_class Shell_SecondaryTrayWnd  ; マルチモニター用
        TaskbarVisible := true
        TrayTip, タスクバー, 表示しました (Ctrl+Shift+A で非表示), 2, 1
    }
}

; Ctrl+Shift+Esc でスクリプト終了（緊急用）
^+Esc::ExitApp