all:
	# !! python setup.py build_ext --inplace
	gcc \
	-I/Users/kai.zhu/AppData/Local/Programs/Python/Python310/include \
	-c \
	-fPIC \
	-o hello.o \
	hello.c
	# !! ar rc hello.pyd hello.o
	# !! ranlib hello.pyd
	gcc \
	-L/Users/kai.zhu/AppData/Local/Programs/Python/Python310/libs \
    -fPIC \
    -o hello.pyd \
    -shared \
    hello.o

clean:
	rm -rf *.out *.bin *.exe *.o *.a *.so test build
