## Install

```bash
pip -r requirements.txt
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

