
run: bin/python install
	$< main.py

install: bin/pip
	$< install -r requirements.txt

bin/pip:
	$(MAKE) __virtualenv

bin/python:
	$(MAKE) __virtualenv

__virtualenv:
	virtualenv -p python3 .
