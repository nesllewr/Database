#define _CRT_SECURE_NO_WARNINGS
#define MAX 1024

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <io.h>

void select(FILE* fp);
void insert(FILE* fp);
void update(FILE* fp);
void delete(FILE* fp);

int main(int argc, char *argv[]) {

	int choice;
	int data_size = 0 ;
	char *ch = (char*) malloc(sizeof(char) * MAX);

	FILE *forigin = NULL;
	FILE *fp = NULL;
	char *file_name = "./pr.csv";

	forigin = fopen("contact2.csv", "r");
	
	
	if (_access(file_name, 2) == 0) {
		printf("already copy contact.csv into %s\n", file_name);
		fp = fopen("./pr.csv", "r+");
	}
	else {
		if (forigin != NULL) {
			fp = fopen(file_name, "w+");
			printf("Data LOADING...\n");
			while ((fgets(ch, MAX, forigin)) != NULL) {
				fprintf(fp, "%s", ch);
			}
		}
		free(ch);
	}

	fclose(forigin);


	if (fp != NULL) {
		
		//연락처 기능 수행
		while (1) {
			printf("\nFUNCTION : ENTER NUMBER\n");
			printf("1. SELECT\n"
					"2. INSERT\n"
					"3. UPDATE\n"
					"4. DELETE\n"
					"5. END\n");
			scanf("%d", &choice);

			if (choice == 5) {
				printf("\nDATABASE SYSTEM END\n");
				break;
			}

			rewind(fp);

			switch (choice) {
			case 1:
				printf("	1. SELECT\n");
				select(fp);
				break;
			case 2:
				fseek(fp, 0, SEEK_END);
				printf("	2. INSERT\n");
				insert(fp);
				break;
			case 3:
				printf("	3. UPDATE\n");
				update(fp);
				break;
			case 4:
				printf("	4. DELETE\n");
				delete(fp);
				break;
			default:
				printf("\nREENTER NUMBER BETWEEN 1~5\n");
			}
		}
	}

	fclose(fp);

	system("pause");

	return 0;
}


void select(FILE* fp) {

	char input[10], data[50];
	char search[38];
	char *name, *number;
	int count = 0, mode;

	printf("name OR number\n");
	scanf("%s", input);

	if (!strcmp(input, "name")) mode = 0;
	else if (!strcmp(input, "number")) mode = 1;
	else return;
	
	char *mode_c = (mode == 0) ? "name" : "number";

	printf(" %s mode SEARCH: ", mode_c);
	scanf("%s", search);

	while (1) {
		if (fgets(data, sizeof(data), fp) == NULL) 	break;
		
		name = strtok(data, ",");
		number = strtok(NULL, ",");

		if ((mode == 0 && strstr(name, search)) || (mode == 1 && strstr(number, search))) {
			printf("%s %s\n", name, number);
			count++;
		}
	}
	printf("total : %d\n", count);
}

void insert(FILE* fp) {

	char name[50], number[12];

	printf("insert NAME : ");
	scanf("%s", name);
	printf("insert NUMBER : ");
	scanf("%s", number);

	fprintf(fp, "\n%s,%s", name, number);
}

void update(FILE* fp) {

	char input[10], data[50];
	char update[38], *ptr;
	char *name, *number;
	int mode;
	long seek;
	char newupdate[38];

	printf("NAME or NUMBER\n");
	scanf("%s", input);

	if (!strcmp(input, "name")) mode = 0;
	else if (!strcmp(input, "number")) mode = 1;
	else return;

	char *mode_c = (mode == 0) ? "name" : "number";

	printf("%s mode UPDATE: ", mode_c);
	scanf("%s", update);
	
	while (1) {

		seek = ftell(fp);
		
		if (fgets(data, sizeof(data), fp) == NULL) {
			printf("There is no such %s in this database system.\n", mode_c);
			break;
		}

		name = strtok(data, ",");
		number = strtok(NULL, ",");	
		
		if ((mode == 0 && !strcmp(name, update)) || (mode == 1 && !strcmp(number, update))) {
			
			printf("updating %s %s with : ", name, number);
			memset(update, '\0', sizeof(update));

			scanf("%s", update);

			ptr = strstr(name, name);
			memcpy(ptr, update, strlen(update) + 1);
			printf("SEEK : %d\n", seek);
			fseek(fp, seek, SEEK_SET);
			fprintf(fp, "%s,%s", name, number);
			fflush(fp);
			
		}
	}
	
}

void delete(FILE* fp) {

	char input[10], data[50];
	char search[38];
	char *name, *number;
	int mode;
	long start, len;

	printf("NAME or NUMBER\n");
	scanf("%s", input);

	if (!strcmp(input, "name")) mode = 0;
	else if (!strcmp(input, "number")) mode = 1;
	else return;

	char *mode_c = (mode == 0) ? "name" : "number";

	printf("%s mode SEARCH: ", mode_c);
	scanf("%s", search);

	while (1) {

		start = ftell(fp);

		if (fgets(data, sizeof(data), fp) == NULL) {
			printf("There is no such %s in this database system.\n", mode_c);
			break;
		}

		//end = ftell(fp);
		//printf("fp tell %d %d\n", start, end);

		name = strtok(data, ",");
		number = strtok(NULL, ",");

		if (mode == 0 && !strcmp(name, search)) {
			printf("deleting %s %s\n", name, number);
			len = _filelength(_fileno(fp)) - ftell(fp);
			char *tmp = (char*)malloc(len);
			len = fread(tmp, 1, len, fp);

			fseek(fp, start, SEEK_SET);
			fwrite(tmp, 1, len, fp);
			fflush(fp);
			free(tmp);
			_chsize(fileno(fp),ftell(fp));
			
			break;
		}
		if (mode == 1 && !strcmp(number, search)) {
			printf("deleting %s %s\n", name, number);

			break;
		}

	}
}
