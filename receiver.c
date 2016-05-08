/*I have referred from the following websites for this part of the code
http://www.thegeekstuff.com/2011/12/c-socket-programming/
http://stackoverflow.com/questions/4139405/how-can-i-get-to-know-the-ip-address-for-interfaces-in-c
http://developerweb.net/viewtopic.php?id=2933
*/

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

#define MAXDATASIZE 65536
#define min(a, b) (((a) < (b)) ? (a) : (b)) 
#define max(a, b) (((a) > (b)) ? (a) : (b)) 

typedef struct{
    uint16_t port_number;
}trace_file;

int command_parser(trace_file *input, FILE *fp) {
    
    char *buf;
    char *start_ptr, *tab_ptr;

    buf = (char *)malloc(MAXDATASIZE * sizeof(char));
    
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
        input->port_number = atoi(start_ptr);
        printf("PortNumber : %d\n",input->port_number);

    } while(tab_ptr != NULL);    
    return 0;
}

int main(int argc, char *argv[])
{
    fd_set readset, tempset;
    trace_file input;
    FILE *fp;
    int listenfd[25], connfd = 0, count = 0, loop = 0, maxfd = 0;
    struct sockaddr_in serv_addr; 
    int bytes_received = 0, result = 0, number_of_lines = 0;
    char recvBuff[MAXDATASIZE];
    int return_value, optval;
    
    if(argc != 2)
    {
        printf("\n Usage: %s <path for tracefile> \n",argv[0]);
        return 1;
    }    

    fp = fopen(argv[1], "r");
    if(fp == NULL) {
        perror("Error while reading tracefile\n");
    }
    memset(listenfd,0,sizeof(listenfd));
    FD_ZERO(&readset);
    FD_ZERO(&tempset);
    
    while(1)
    {
        if(feof(fp))
            break;
        return_value = command_parser(&input,fp);
        if(return_value)
            break;
        
        listenfd[number_of_lines] = socket(AF_INET, SOCK_STREAM, 0);
        maxfd = max(maxfd, listenfd[number_of_lines]);
        FD_SET(listenfd[number_of_lines], &readset);
        
        memset(&serv_addr, '0', sizeof(serv_addr));
        memset(recvBuff, '0', sizeof(recvBuff)); 

        serv_addr.sin_family = AF_INET;
        serv_addr.sin_addr.s_addr = htonl(INADDR_ANY);
        serv_addr.sin_port = htons(input.port_number); 

        optval = 1;
        setsockopt(listenfd[number_of_lines], SOL_SOCKET, SO_REUSEPORT, &optval, sizeof(optval));
    
        bind(listenfd[number_of_lines], (struct sockaddr*)&serv_addr, sizeof(serv_addr)); 

        listen(listenfd[number_of_lines], 200); 
        number_of_lines++;
    }
    
    while(1)
    {
        memcpy(&tempset,&readset,sizeof(tempset));
        result = select(maxfd + 1, &tempset, NULL, NULL, NULL);
        
        if(result <= 0) {
            printf("Error in select\n");
        } else if(result > 0) {
            for(count = 0; count < number_of_lines; count++) {
                if(FD_ISSET(listenfd[count], &tempset)) {
                    connfd = accept(listenfd[count], (struct sockaddr*)NULL, NULL); 
                    if(connfd < 0) {
                        printf("Error in accept\n");
                    } else {
                        FD_SET(connfd, &readset);
                        maxfd = max(maxfd, connfd);
                    }
                    FD_CLR(listenfd[count], &tempset);
                }
            }
        
            for(loop = 0; loop < maxfd + 1; loop++) {
                if(FD_ISSET(loop, &tempset)) {
                    do {
                        bytes_received = recv(loop, recvBuff, MAXDATASIZE,0); 
                        //printf("bytes :%d\n",bytes_received);
                    }while(bytes_received == -1 && errno == EINTR);
                    
                    // if(fputs(recvBuff, stdout) == EOF)
                    // {
                        // printf("\n Error : Fputs error\n");
                    // }
                }
            }
        }
        //close(connfd);
        //sleep(1);
    }
     
    return 0;
}