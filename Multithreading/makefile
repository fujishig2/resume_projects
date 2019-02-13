CC = gcc -g -Wall -c

a4tasks: main.o check_args.o interp_file.o create_threads.o
	gcc -o $@ $^ -lpthread -lrt

%.o: %.c
	$(CC) $^

clean:
	rm *.o a4tasks

tar:
	tar -cvf submit.tar *.c *.h *.o a4tasks makefile CMPUT379\ Ass4.pdf
