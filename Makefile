all: sender receiver

sender: sender.o
	gcc -o sender.exe -g sender.o

receiver: receiver.o
	gcc -o receiver.exe -g receiver.o

sender.o: sender.c
	gcc -g -c -Wall sender.c

receiver.o: receiver.c
	gcc -g -c -Wall receiver.c
    
clean:
	rm -f *.o sender.exe receiver.exe