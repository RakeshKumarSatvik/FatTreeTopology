#include <sys/socket.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <time.h> 

#define MAXDATASIZE 1500

typedef struct{
    uint16_t port_number;
}trace_file;

void command_parser(trace_file *input, FILE *fp) {
    
    char buf[MAXDATASIZE];
    char *start_ptr, *tab_ptr;

    printf("\nReading from the file.\n");
    fgets(buf,80,fp);
    tab_ptr = buf;
    do {
        start_ptr = tab_ptr;
        tab_ptr = strchr(start_ptr, ' ');
        if (tab_ptr != NULL) {
         *tab_ptr++ = '\0';
        }
        input->port_number = atoi(start_ptr);
        printf("PortNumber : %d\n",input->port_number);

    } while(tab_ptr != NULL);    
}

int main(int argc, char *argv[])
{
    trace_file input;
    FILE *fp;
    int listenfd = 0, connfd = 0;
    struct sockaddr_in serv_addr; 
    int bytes_received = 0;
    char recvBuff[MAXDATASIZE];

    if(argc != 2)
    {
        printf("\n Usage: %s <path for tracefile> \n",argv[0]);
        return 1;
    }    

    fp = fopen(argv[1], "r");
    if(fp == NULL) {
        perror("Error while reading tracefile\n");
    }
    
    while(1)
    {
        if(feof(fp))
            break;
        command_parser(&input,fp);

        listenfd = socket(AF_INET, SOCK_STREAM, 0);
        memset(&serv_addr, '0', sizeof(serv_addr));
        memset(recvBuff, '0', sizeof(recvBuff)); 

        serv_addr.sin_family = AF_INET;
        serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
        serv_addr.sin_port = htons(input.port_number); 

        bind(listenfd, (struct sockaddr*)&serv_addr, sizeof(serv_addr)); 

        listen(listenfd, 35); 

        while(1)
        {
            connfd = accept(listenfd, (struct sockaddr*)NULL, NULL); 
            
            do {
                bytes_received = recv(connfd, recvBuff, MAXDATASIZE,0); 
                //printf("bytes :%d\n",bytes_received);
            }while(bytes_received > 0);
            
            if(fputs(recvBuff, stdout) == EOF)
            {
                printf("\n Error : Fputs error\n");
            }
            
            //close(connfd);
            //sleep(1);
         }
    }
    return 0;
}