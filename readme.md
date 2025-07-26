## Install

```bash
pip install .
```

## Launch It

```bash
python main.py
```

## Generate the UI python file

```bash
pyside6-uic bot/ui/mainwindow.ui -o bot/ui/mainwindow.py
```

## Generate the exec

````bash
pyinstaller nwbot.spec

## TODO

[X] Drag and drop
[X] Right and left click
[] Responsive layout
[X] Missing Keys
[X] Remove Keys with suppr
[] Unbound by window record with pynput
[X] Export logfile
[] Insert time beetwen keys