.PHONY: all test clean

build:
	cd hwcomponents_cacti/cacti && \
		sed -i 's/-m64//g;s/-gstabs+//g' cacti.mk && \
		make clean && make
	chmod -R 775 hwcomponents_cacti/cacti || true
	test -x hwcomponents_cacti/cacti/cacti

install:
	make build
	pip3 install .
