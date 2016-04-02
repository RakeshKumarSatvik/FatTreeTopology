#include<stdio.h>
#include<string.h>
#include<stdlib.h>

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
    while(fgets(buf,80,fp) != NULL) {
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
        break;
    }
    
}

int main() {
    trace_file input;
    FILE *fp;
    
    fp = fopen("traffic/test.trace", "r");
    if(fp == NULL) {
        perror("Error while reading tracefile\n");
    }

    command_parser(&input,fp);
    
    printf("Destination : %s\nPort number : %s\nFile Size : %s\n",input.destination_ip,input.port_number,input.file_size);

    command_parser(&input,fp);
    
    printf("Destination : %s\nPort number : %s\nFile Size : %s\n",input.destination_ip,input.port_number,input.file_size);

    return 0;
}