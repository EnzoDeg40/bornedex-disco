PYTHON = python3
PIP = pip3
REQUIREMENTS = requirements.txt

all: run

install:
	$(PIP) install -r requirements.txt
	$(PYTHON) init.py

run:
	$(PYTHON) serv.py

clean:
	rm -rf __pycache__

.PHONY: all install run clean
