## Get the latest release

<https://github.com/zelazna/nw_bot/releases/latest>

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

```bash
pyinstaller nwbot.spec
```

## Run tests

```bash
pytest --cov=bot --cov-report=term --cov-report=xml
```

## TODO

- [X] Drag and drop
- [X] Right and left click
- [X] Missing Keys
- [X] Remove Keys with suppr
- [X] Export logfile
- [X] Unbound by window record with pynput
- [X] Responsive layout
- [ ] Insert time beetwen keys
- [ ] Command pattern
- [ ] Copy and paste Keys
