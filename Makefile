.PHONY: all test clean

build:
	cd hwcomponents_cacti/cacti && \
		sed 's/-m64//g;s/-gstabs+//g' cacti.mk > cacti.mk.tmp && \
		mv cacti.mk.tmp cacti.mk && \
		sed 's/"\."VER_/"." VER_/g' io.cc > io.cc.tmp && \
		mv io.cc.tmp io.cc && \
		make clean && make
	chmod -R 775 hwcomponents_cacti/cacti || true
	test -x hwcomponents_cacti/cacti/cacti

install:
	make build
	pip3 install .
