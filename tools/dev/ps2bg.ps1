# Drives the RIPPS2 lab PCSX2 in the BACKGROUND: it never takes focus, never touches the keyboard, and stays off the
# screen, so the user can keep using the PC (or play a game) while tests run. Same step language as ps2drive.ps1.
#
#   ps2bg.ps1 -Elf <path> -Steps "wait:24,start,wait:2,grab,cross,wait:3,grab" [-Keep] [-Attach]
#
# How: PCSX2 is started minimized without activation (SW_SHOWMINNOACTIVE), then restored, still without activation,
# to a spot far off the screen, so it renders but nobody sees it. Pad buttons are POSTED to PCSX2's own windows as
# key messages (the [Pad1] keyboard bindings), so no other program ever receives them. "grab" asks the window to
# draw itself into a bitmap (PrintWindow, PW_RENDERFULLCONTENT), which works off screen. "rec" posts F11 (PCSX2's
# video capture), "shot" F8 (its screenshot). At the end the lab PCSX2 is closed (killed: its cards are lab copies).
#
# Step tokens: wait:<sec>, grab, shot, rec, sstate (F1: a save state, for reading a stuck EE), up, down, left, right, cross, circle, square, triangle, start, select,
#              l1, r1, l2, r2, l3, r3, rup/rdown/rleft/rright (right stick), hold:<button>:<ms>,
#              kdown:<button> / kup:<button>
param(
  [string]$Elf,
  [string]$Steps = "wait:15,grab",
  [switch]$Keep,
  [string]$Iso = "",
  [switch]$Attach
)

$lab = "B:\Emulation\PlayStation\PCSX2\ripps2-lab"
$exe = "$lab\pcsx2-qt.exe"
$grabDir = Join-Path $PSScriptRoot "grabs"
New-Item -ItemType Directory -Force $grabDir | Out-Null

Add-Type -AssemblyName System.Drawing
Add-Type -ReferencedAssemblies System.Drawing @"
using System;
using System.Collections.Generic;
using System.Runtime.InteropServices;
using System.Text;
public static class BG {
  [StructLayout(LayoutKind.Sequential, CharSet = CharSet.Unicode)]
  public struct STARTUPINFO { public int cb; public string lpReserved, lpDesktop, lpTitle; public int dwX, dwY, dwXSize, dwYSize,
    dwXCountChars, dwYCountChars, dwFillAttribute, dwFlags; public short wShowWindow, cbReserved2; public IntPtr lpReserved2, hStdInput, hStdOutput, hStdError; }
  [StructLayout(LayoutKind.Sequential)] public struct PROCESS_INFORMATION { public IntPtr hProcess, hThread; public int dwProcessId, dwThreadId; }
  [StructLayout(LayoutKind.Sequential)] public struct POINT { public int X, Y; }
  [StructLayout(LayoutKind.Sequential)] public struct RECT { public int L, T, R, B; }
  [StructLayout(LayoutKind.Sequential)] public struct WINDOWPLACEMENT { public int length, flags, showCmd; public POINT ptMin, ptMax; public RECT rcNormal; }
  [DllImport("kernel32.dll", CharSet = CharSet.Unicode, SetLastError = true)]
  static extern bool CreateProcess(string app, StringBuilder cmd, IntPtr pa, IntPtr ta, bool inherit, uint flags, IntPtr env, string dir,
    ref STARTUPINFO si, out PROCESS_INFORMATION pi);
  [DllImport("kernel32.dll")] static extern bool CloseHandle(IntPtr h);
  public delegate bool EnumProc(IntPtr h, IntPtr l);
  [DllImport("user32.dll")] static extern bool EnumWindows(EnumProc f, IntPtr l);
  [DllImport("user32.dll")] static extern bool EnumChildWindows(IntPtr p, EnumProc f, IntPtr l);
  [DllImport("user32.dll")] static extern uint GetWindowThreadProcessId(IntPtr h, out uint pid);
  [DllImport("user32.dll")] static extern bool IsWindowVisible(IntPtr h);
  [DllImport("user32.dll", CharSet = CharSet.Unicode)] static extern int GetClassName(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll", CharSet = CharSet.Unicode)] static extern int GetWindowText(IntPtr h, StringBuilder s, int n);
  [DllImport("user32.dll")] public static extern bool PostMessage(IntPtr h, uint msg, IntPtr w, IntPtr l);
  [DllImport("user32.dll")] public static extern uint MapVirtualKey(uint code, uint type);
  [DllImport("user32.dll")] public static extern bool GetWindowPlacement(IntPtr h, ref WINDOWPLACEMENT p);
  [DllImport("user32.dll")] public static extern bool SetWindowPlacement(IntPtr h, ref WINDOWPLACEMENT p);
  [DllImport("user32.dll")] public static extern bool GetWindowRect(IntPtr h, out RECT r);
  [DllImport("user32.dll")] public static extern bool PrintWindow(IntPtr h, IntPtr hdc, uint flags);
  [DllImport("user32.dll")] public static extern IntPtr GetForegroundWindow();
  [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)] static extern IntPtr CreateDesktop(string name, IntPtr dev, IntPtr mode, int flags, uint access, IntPtr sa);
  [DllImport("user32.dll", CharSet = CharSet.Unicode, SetLastError = true)] static extern IntPtr OpenDesktop(string name, int flags, bool inherit, uint access);
  [DllImport("user32.dll", SetLastError = true)] static extern bool SetThreadDesktop(IntPtr h);
  [DllImport("user32.dll")] static extern bool EnumDesktopWindows(IntPtr desk, EnumProc f, IntPtr l);

  // A desktop of its own (not the one on the screen): nothing on it can take the focus, show up or get the keyboard
  public static string DeskName = "RIPPS2LAB";
  public static IntPtr Desk = IntPtr.Zero;
  public static bool UseDesk = false;
  public static bool OpenDesk() {
    Desk = OpenDesktop(DeskName, 0, false, 0x10000000); // GENERIC_ALL
    if (Desk == IntPtr.Zero) Desk = CreateDesktop(DeskName, IntPtr.Zero, IntPtr.Zero, 0, 0x10000000, IntPtr.Zero);
    UseDesk = Desk != IntPtr.Zero;
    return UseDesk;
  }
  // Runs f on a thread that sits on the lab's desktop (window messages only cross within one desktop)
  public static void OnDesk(Action f) {
    if (!UseDesk) { f(); return; }
    Exception err = null;
    var t = new System.Threading.Thread(() => { try { SetThreadDesktop(Desk); f(); } catch (Exception e) { err = e; } });
    t.Start(); t.Join();
    if (err != null) throw err;
  }
  public static IntPtr MainWindowOnDesk(int pid) {
    if (!UseDesk) return MainWindow(pid);
    IntPtr best = IntPtr.Zero; long area = 0;
    EnumDesktopWindows(Desk, (h, l) => { uint p; GetWindowThreadProcessId(h, out p);
      if (p == pid && IsWindowVisible(h)) { RECT r; GetWindowRect(h, out r); long a = (long)(r.R - r.L) * (r.B - r.T);
        var c = new StringBuilder(64); GetClassName(h, c, 64);
        if (a > area && c.ToString().StartsWith("Qt")) { area = a; best = h; } }
      return true; }, IntPtr.Zero);
    return best;
  }
  public static void Post(IntPtr h, uint msg, long w, long l) { OnDesk(() => PostMessage(h, msg, (IntPtr)w, (IntPtr)l)); }
  public static bool GrabOnDesk(IntPtr h, string file) { bool ok = false; OnDesk(() => { ok = Grab(h, file); }); return ok; }
  public static void ParkOnDesk(IntPtr h, int w, int hgt) { OnDesk(() => Park(h, w, hgt)); }

  public static int Launch(string exe, string args, string dir) {
    var si = new STARTUPINFO(); si.cb = Marshal.SizeOf(si); si.dwFlags = 1; si.wShowWindow = 7; // STARTF_USESHOWWINDOW, SW_SHOWMINNOACTIVE
    if (UseDesk) si.lpDesktop = "WinSta0\\" + DeskName;
    PROCESS_INFORMATION pi;
    if (!CreateProcess(exe, new StringBuilder("\"" + exe + "\" " + args), IntPtr.Zero, IntPtr.Zero, false, 0, IntPtr.Zero, dir, ref si, out pi)) return -1;
    CloseHandle(pi.hThread); CloseHandle(pi.hProcess);
    return pi.dwProcessId;
  }
  public static string Info(IntPtr h) {
    var c = new StringBuilder(128); GetClassName(h, c, 128); var t = new StringBuilder(128); GetWindowText(h, t, 128);
    return c.ToString() + " '" + t.ToString() + "'";
  }
  // The process's main window: its biggest visible top-level window (the game display lives inside it)
  public static IntPtr MainWindow(int pid) {
    IntPtr best = IntPtr.Zero; long area = 0;
    EnumWindows((h, l) => { uint p; GetWindowThreadProcessId(h, out p);
      if (p == pid && IsWindowVisible(h)) { RECT r; GetWindowRect(h, out r); long a = (long)(r.R - r.L) * (r.B - r.T);
        var c = new StringBuilder(64); GetClassName(h, c, 64);
        if (a > area && c.ToString().StartsWith("Qt")) { area = a; best = h; } }
      return true; }, IntPtr.Zero);
    return best;
  }
  public static List<IntPtr> Children(IntPtr parent) {
    var list = new List<IntPtr>();
    EnumChildWindows(parent, (h, l) => { list.Add(h); return true; }, IntPtr.Zero);
    return list;
  }
  // Somewhere nobody looks: restored (so it renders) far off every screen, and never activated
  public static void Park(IntPtr h, int w, int hgt) {
    var p = new WINDOWPLACEMENT(); p.length = Marshal.SizeOf(p); GetWindowPlacement(h, ref p);
    p.showCmd = 4; // SW_SHOWNOACTIVATE
    p.rcNormal.L = -12000; p.rcNormal.T = -9000; p.rcNormal.R = -12000 + w; p.rcNormal.B = -9000 + hgt;
    SetWindowPlacement(h, ref p);
  }
  public static bool Grab(IntPtr h, string file) {
    RECT r; GetWindowRect(h, out r); int w = r.R - r.L, hh = r.B - r.T;
    if (w <= 0 || hh <= 0) return false;
    using (var bmp = new System.Drawing.Bitmap(w, hh)) {
      using (var g = System.Drawing.Graphics.FromImage(bmp)) { IntPtr dc = g.GetHdc(); PrintWindow(h, dc, 2); g.ReleaseHdc(dc); }
      bmp.Save(file, System.Drawing.Imaging.ImageFormat.Png);
    }
    return true;
  }
}
"@

$vk = @{ up=0x26; down=0x28; left=0x25; right=0x27; cross=0x58; circle=0x43; square=0x5A; triangle=0x53;
         start=0x0D; select=0x08; l1=0x51; r1=0x45; l2=0x31; r2=0x33; f8=0x77; f1=0x70; rec=0x7A; l3=0x56; r3=0x42;
         rup=0x49; rdown=0x4B; rleft=0x4A; rright=0x4C }
$extended = @(0x25, 0x26, 0x27, 0x28)

function KeyMsg([IntPtr]$h, [int]$code, [bool]$up) {
  $scan = [BG]::MapVirtualKey($code, 0)
  $l = 1 -bor ($scan -shl 16)
  if ($extended -contains $code) { $l = $l -bor (1 -shl 24) }
  if ($up) { $l = $l -bor (1 -shl 30) -bor (1 -shl 31) }
  $msg = if ($up) { 0x0101 } else { 0x0100 } # WM_KEYUP / WM_KEYDOWN
  [BG]::Post($h, $msg, [int64]$code, [int64]([uint32]$l))
}
# The key goes to every window of PCSX2's main window (the frame and the display inside it); Qt delivers it to the
# widget that holds the window's focus, which is the game display.
function Targets {
  switch ($env:PS2BG_TARGET) {
    'children' { return @([BG]::Children($script:main)) }
    'all' { $t = @($script:main); $t += [BG]::Children($script:main); return $t }
    default { return @($script:main) } # the frame: Qt hands the key to the game display, which holds its focus
  }
}
function Down([int]$code) { foreach ($h in (Targets)) { KeyMsg $h $code $false } }
function Up([int]$code) { foreach ($h in (Targets)) { KeyMsg $h $code $true } }
function Press([int]$code, [int]$ms = 100) { Down $code; Start-Sleep -Milliseconds $ms; Up $code; Start-Sleep -Milliseconds 120 }

if ($Attach) {
  $p = Get-Process pcsx2-qt -ErrorAction SilentlyContinue | Where-Object { $_.Path -eq $exe } | Select-Object -First 1
  if (-not $p) { "no running lab PCSX2 to attach to"; return }
  $pid2 = $p.Id; "attached to pid $pid2"
} else {
  $fgBefore = [BG]::GetForegroundWindow()
  if (-not $env:PS2BG_NODESK) { if ([BG]::OpenDesk()) { "on the lab's own desktop ($([BG]::DeskName)): it cannot take the focus or show" } else { "could not make the lab desktop; running parked off screen" } }
  $launchArgs = "-fastboot -elf `"$Elf`""
  if ($Iso) { $launchArgs += " `"$Iso`"" }
  $pid2 = [BG]::Launch($exe, $launchArgs, $lab)
  if ($pid2 -le 0) { "could not start PCSX2"; return }
  "launched pid $pid2 (minimized, not activated)"
}
$script:main = [IntPtr]::Zero
for ($i = 0; $i -lt 60 -and $script:main -eq [IntPtr]::Zero; $i++) { Start-Sleep -Milliseconds 250; $script:main = [BG]::MainWindowOnDesk($pid2) }
if ($script:main -eq [IntPtr]::Zero) { "no PCSX2 window appeared"; return }
if (-not $Attach) {
  Start-Sleep -Milliseconds 400
  [BG]::ParkOnDesk($script:main, 1300, 1060)
  "parked off screen: $([BG]::Info($script:main))"
  if ([BG]::GetForegroundWindow() -ne $fgBefore) { "note: the foreground window changed during launch" }
}
Press 0x10 # an unbound key (Shift) first, so the first real press is not lost

foreach ($s in ($Steps -split ',')) {
  $s = $s.Trim(); if (-not $s) { continue }
  if ($s -like 'wait:*') { Start-Sleep -Seconds ([double]($s.Split(':')[1])); continue }
  if ($s -eq 'grab') {
    $file = Join-Path $grabDir ("grab_{0}.png" -f (Get-Date -Format 'HHmmss_fff'))
    if ([BG]::GrabOnDesk($script:main, $file)) { "grab $file" } else { "grab failed" }
    continue
  }
  if ($s -eq 'shot') { Press $vk.f8; Start-Sleep -Milliseconds 1300; "shot"; continue }
  if ($s -eq 'sstate') { Press $vk.f1; Start-Sleep -Milliseconds 2500; "save state (F1, lab sstates)"; continue }
  if ($s -like 'kdown:*') { Down $vk[$s.Split(':')[1]]; "kdown $($s.Split(':')[1])"; continue }
  if ($s -like 'kup:*') { Up $vk[$s.Split(':')[1]]; "kup $($s.Split(':')[1])"; continue }
  if ($s -like 'hold:*') { $a = $s.Split(':'); Press $vk[$a[1]] ([int]$a[2]); "hold $($a[1])"; continue }
  if ($vk.ContainsKey($s)) { Press $vk[$s]; "press $s" } else { "unknown step '$s'" }
}

if (-not $Keep) {
  Stop-Process -Id $pid2 -Force -ErrorAction SilentlyContinue
  "PCSX2 closed"
}
