#include<stdio.h>

#include<string.h>

#include<stdlib.h>

#include <sys/socket.h>

#include <netinet/in.h>

#include <arpa/inet.h>

#include <unistd.h>

#include <errno.h>

#include <sys/types.h>

#include <time.h>



#define MAXDATASIZE 1024



typedef struct{

    char destination_ip[80];

    char port_number[80];

    char file_size[80];

}trace_file;



void command_parser(trace_file *input, FILE *fp) {

    

    char buf[MAXDATASIZE];

    char *start_ptr, *tab_ptr;

    int count = 0;



    printf("\nReading from the file.\n");

    fgets(buf,80,fp);

    tab_ptr = buf;

    do {

        start_ptr = tab_ptr;

        tab_ptr = strchr(start_ptr, ' ');

        if (tab_ptr != NULL) {

         *tab_ptr++ = '\0';

        }

        

        switch(count){

            case 1: strcpy(input->destination_ip, start_ptr);

                    break;

            case 3: strcpy(input->port_number, start_ptr);

                    break;

            case 5: strcpy(input->file_size,start_ptr);

                    break;                        

        }

        

        count++;

    } while(tab_ptr != NULL);    

}



int main(int argc, char *argv[]) {

    trace_file input;

    FILE *fp;

    int listenfd = 0, connfd = 0;

    struct sockaddr_in sender_addr;

    

    char sendBuff[1025];

    time_t ticks;

    

    fp = fopen(argv[1], "r");

    if(fp == NULL) {

        perror("Error while reading tracefile\n");

    }



    command_parser(&input,fp);

    

    printf("Destination : %s\nPort number : %s\nFile Size : %s\n",input.destination_ip,input.port_number,input.file_size);



    command_parser(&input,fp);

    

    printf("Destination : %s\nPort number : %s\nFile Size : %s\n",input.destination_ip,input.port_number,input.file_size);

    

    sender_addr.sin_family = AF_INET;

    sender_addr.sin_addr.s_addr = htonl(INADDR_ANY);

    sender_addr.sin_port = htons(5000); 



    listenfd = socket(AF_INET, SOCK_STREAM, 0);

    memset(&sender_addr, '0', sizeof(sender_addr));

    memset(sendBuff, '0', sizeof(sendBuff)); 

    

    bind(listenfd, (struct sockaddr*)&sender_addr, sizeof(sender_addr)); 



    listen(listenfd, 10); 



    while(1)

    {

        connfd = accept(listenfd, (struct sockaddr*)NULL, NULL); 



        ticks = time(NULL);

        snprintf(sendBuff, sizeof(sendBuff), "%.24s\r\n", ctime(&ticks));

        write(connfd, sendBuff, strlen(sendBuff)); 



        close(connfd);

        sleep(1);

    }

     

    return 0;

}