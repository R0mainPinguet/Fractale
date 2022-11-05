CC = gcc
RM = rm -f
CFLAGS = -ansi -Wall -pedantic -O3 -lm -fopenmp -c
LFLAGS = -lm -O3 -fopenmp
EXEC = main_serial.out main_parallel.out

.PHONY: clean fclean

all: $(EXEC)

%.out: %.o
	$(CC) -o $@ $^ $(LFLAGS)

%.o: %.c
	$(CC) -o $@ $(CFLAGS) $<

julia.o: julia.c julia.h

main_serial.o: main_serial.c julia.o
main_parallel.o: main_parallel.c julia.o

main_serial.out: main_serial.o julia.o
main_parallel.out: main_parallel.o julia.o

clean:
	$(RM) *.o
	$(RM) *~

fclean: clean
	$(RM) $(EXEC)
