# FakeUpdate

A harmless macOS-style update-screen simulator. It does **not** install updates,
change system files, lock the Mac, or restart the computer.

## Run
```bash
python3 fakeupdate.py
```

## Create a Desktop shortcut and launch
```bash
chmod +x install.command
./install.command
```

Controls: `F11` toggles fullscreen; `Esc` exits.
Requires Python 3 with Tkinter. On many macOS Python installations Tkinter is included.
