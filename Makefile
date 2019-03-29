CXX=		g++
CXXFLAGS=	-g -Wall -std=gnu++11
SHELL=		bash

all:		luasocket luafs

luasocket:
	cd contrib/luasocket; \
	make
	cp contrib/luasocket/src/*.so lib/
	@echo Symbolically linking shared objects
	cd lib; \
	ln -s socket-*.so socket.so; \
	ln -s mime-*.so mime.so

luafs:
	cd contrib/luafs; \
	make
	cp contrib/luafs/src/*.so lib/

clean:
	cd contrib/luasocket; \
	make clean
	cd contrib/luafs; \
	make clean
	rm -rf lib/*.so
