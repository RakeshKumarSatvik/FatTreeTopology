#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <netdb.h>
#include <unistd.h>
#include <errno.h>
#include <arpa/inet.h>
#include <math.h>

#define MAXDATASIZE 1500
#define min(a, b) (((a) < (b)) ? (a) : (b))

typedef struct{
    char destination_ip[80];
    uint16_t port_number;
    int file_size;
}trace_file;

int command_parser(trace_file *input, FILE *fp) {
    
    char buf[MAXDATASIZE];
    char *start_ptr, *tab_ptr;
    int count = 0;
    char *comp, comp1;
    
    if(fgets(buf,80,fp) == NULL)
        return 1;
    printf("\nReading from the file.\n");
    
    tab_ptr = buf;
    do {
        start_ptr = tab_ptr;
        tab_ptr = strchr(start_ptr, ' ');
        if (tab_ptr != NULL) {
         *tab_ptr++ = '\0';
        }

        switch(count){
            case 1: strcpy(input->destination_ip, start_ptr);
                    printf("Destination : %s\n",input->destination_ip);
                    break;
            case 3: input->port_number = atoi(start_ptr);
                    printf("Port Number : %d\n",input->port_number);
                    break;
            case 5: input->file_size = 1;
                    input->file_size = atoi(start_ptr);
                    comp = start_ptr+strlen(start_ptr)-1;
                    strcpy(&comp1,start_ptr+strlen(start_ptr)-2);
                    // printf("comp : %s start_ptr : %s comp1 : %c strcmp : %d ",comp,start_ptr,comp1,strcmp(&comp1,"M"));
                    if(strcmp(comp,"M") == 0 || strcmp(&comp1,"M") == 1){
                        input->file_size *= pow(10,6);
                    } else if(strcmp(comp,"K") == 0 || strcmp(&comp1,"K") == 1) {
                        input->file_size *= pow(10,3);
                    } else if(strcmp(comp,"G") == 0 || strcmp(&comp1,"G") == 1) {
                        input->file_size *= pow(10,9);
                    }
                    printf("File Size : %d\n",input->file_size);
                    break;
        }
        count++;
    } while(tab_ptr != NULL);    
    return 0;
}

int main(int argc, char *argv[]) {
    trace_file input;
    FILE *fp;
    struct sockaddr_in sender_addr;
    int bytes_to_write = 0, bytes_written = 0, remaining_bytes = 0;
    int sockfd = 0, return_value = 0;
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
        return_value = command_parser(&input,fp);
        if(return_value)
            break;
                
        memset(recvBuff, '0',sizeof(recvBuff));
        if((sockfd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
        {
            printf("\n Error : Could not create socket \n");
            return 1;
        }

        memset(&sender_addr, '0', sizeof(sender_addr)); 

        sender_addr.sin_family = AF_INET;
        sender_addr.sin_port = htons(input.port_number);

        if(inet_pton(AF_INET, input.destination_ip, &sender_addr.sin_addr)<=0)
        {
            printf("\n inet_pton error occured\n");
            return 1;
        }

        if(connect(sockfd, (struct sockaddr *)&sender_addr, sizeof(sender_addr)) < 0)
        {
           printf("\n Error : Connect Failed \n");
           return 1;
        }

        snprintf(recvBuff, sizeof(recvBuff), "Hello World!!\n");
        remaining_bytes = input.file_size;
        
        while(remaining_bytes > 0) {
            bytes_to_write = min(MAXDATASIZE, remaining_bytes);
            bytes_written = send(sockfd, recvBuff, bytes_to_write,0);
            remaining_bytes -= bytes_written;
            // printf("Reached here %d file size : %d bytes_written : %d\n",remaining_bytes,input.file_size,bytes_written);
        }
        
        if(remaining_bytes > 0)
        {
            printf("\n Send error, bytes_remaining : %d\n",remaining_bytes);
        } 
    }
    return 0;
}