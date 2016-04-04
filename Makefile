all: sender receiver

sender: sender.o
	gcc -o sender -g sender.o -lpthread

receiver: receiver.o
	gcc -o receiver -g receiver.o

sender.o: sender.c
	gcc -g -c -Wall sender.c

receiver.o: receiver.c
	gcc -g -c -Wall receiver.c
    
clean:
	rm -f *.o sender receiver