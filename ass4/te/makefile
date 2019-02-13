a4tasks: main.o check_args.o interp_file.o create_threads.o
	gcc -o $@ $^ -lpthread -lrt

main.o: main.c check_args.h interp_file.h
	gcc -g -Wall -c main.c

check_args.o: check_args.c check_args.h
	gcc -g -Wall -c check_args.c

interp_file.o: interp_file.c interp_file.h
	gcc -g -Wall -c interp_file.c

create_threads.o: create_threads.c create_threads.h
	gcc -g -Wall -c create_threads.c

clean:
	rm *.o a4tasks submit.tar

tar:
	tar -cvf submit.tar *.c *.h *.o a4tasks makefile CMPUT379\ Ass4.pdf
