VENV=.venv
PYTHON=$(VENV)\Scripts\python.exe
PIP=$(VENV)\Scripts\pip.exe

.PHONY: install run clean

install:
	python -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

run:
	$(PYTHON) app.py

clean:
	if exist $(VENV) rmdir /s /q $(VENV)