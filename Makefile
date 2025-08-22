.PHONY: all test clean

build:
	cd hwcomponents_cacti/cacti && make clean && make
	chmod -R 775 hwcomponents_cacti/cacti || true
	test -x hwcomponents_cacti/cacti/cacti

install:
	make build
	pip3 install .
