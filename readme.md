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

[] Drag and drop
[] Right and left click
[] Responsive layout
[] Missing Keys
[] Remove Keys with suppr
[] Unbound by window record with pynput
[] Export logfile
