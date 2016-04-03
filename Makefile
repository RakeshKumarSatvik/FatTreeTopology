sender.exe: sender.o
	gcc -o sender.exe -g sender.o

sender.o: sender.c
	gcc -g -c -Wall sender.c

clean:
	rm -f *.o sender.exe