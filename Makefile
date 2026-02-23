.PHONY: all test clean

build:
	cd hwcomponents_cacti/cacti && \
		sed -i.bak 's/-m64//g;s/-gstabs+//g' cacti.mk && rm -f cacti.mk.bak && \
		sed -i.bak 's/"\."VER_COMMENT_CACTI/"." VER_COMMENT_CACTI/g' io.cc && rm -f io.cc.bak && \
		make clean && make
	chmod -R 775 hwcomponents_cacti/cacti || true
	test -x hwcomponents_cacti/cacti/cacti

install:
	make build
	pip3 install .
