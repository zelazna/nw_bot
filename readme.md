[![Coverage Status](https://coveralls.io/repos/github/zelazna/nw_bot/badge.svg)](https://coveralls.io/github/zelazna/nw_bot)
[![Unit tests](https://github.com/zelazna/nw_bot/actions/workflows/test.yaml/badge.svg)](https://github.com/zelazna/nw_bot/actions/workflows/test.yaml)

## Get the latest release

<https://github.com/zelazna/nw_bot/releases/latest>

## Install

```bash
pip install .
```

## Launch It

```bash
bot-gui
```

## Generate the UI python file

```bash
pyside6-uic bot/ui/main_window.ui -o bot/ui/main_window.py
```

## Generate the exec

```bash
pyinstaller nwbot.spec
```

## Run tests

```bash
python -m pytest --cov=bot --cov-report=term --cov-report=xml
```
