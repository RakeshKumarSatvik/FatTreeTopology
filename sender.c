#include<stdio.h>
#include<string.h>
#include<stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>

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
    struct sockaddr_in sender_addr;
    
    int sockfd = 0, n = 0;
    char recvBuff[1024];
    time_t ticks; 
    
    if(argc != 2)
    {
        printf("\n Usage: %s <path for tracefile> \n",argv[0]);
        return 1;
    }    

    fp = fopen(argv[1], "r");
    if(fp == NULL) {
        perror("Error while reading tracefile\n");
    }

    command_parser(&input,fp);
    
    printf("Destination : %s\nPort number : %s\nFile Size : %s\n",input.destination_ip,input.port_number,input.file_size);
    
    memset(recvBuff, '0',sizeof(recvBuff));
    if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Error : Could not create socket \n");
        return 1;
    }

    memset(&sender_addr, '0', sizeof(sender_addr)); 

    sender_addr.sin_family = AF_INET;
    sender_addr.sin_port = htons(5000); 

    if(inet_pton(AF_INET, "127.0.0.1", &sender_addr.sin_addr)<=0)
    {
        printf("\n inet_pton error occured\n");
        return 1;
    } 

    if( connect(sockfd, (struct sockaddr *)&sender_addr, sizeof(sender_addr)) < 0)
    {
       printf("\n Error : Connect Failed \n");
       return 1;
    } 

    snprintf(recvBuff, sizeof(recvBuff), "%.24s\r\n", (char *)ctime(&ticks));
    n = write(sockfd, recvBuff, sizeof(recvBuff)-1);
    if(n < 0)
    {
        printf("\n Read error \n");
    } 
    
    return 0;
}