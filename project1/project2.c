#define _CRT_SECURE_NO_WARNINGS
#define MAX 1024

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <io.h>

typedef struct DATA{
	char name[40];
	char number[15];
	int check;
	struct DATA *next;
}DATA;

DATA *head=NULL;

void load(FILE* fp);
void save();

int select();
void insert();
void update(int total);
void delete(int total);

int main(int argc, char *argv[]) {

	int choice, total;
	char *ch = (char*)malloc(sizeof(char) * MAX);

	FILE *forigin = NULL;
	FILE *fp = NULL;
	char *file_name = "2017029552_남은성.csv";

	forigin = fopen("contact2.csv", "r");

	if (_access(file_name, 2) == 0) {
		printf("already copy contact.csv into %s\n", file_name);
		fp = fopen(file_name, "r");
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

	rewind(fp);
	printf("DATA LOADING...");

	load(fp);
	
	fclose(fp);
	
	printf("FINISH");

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
			while (getchar() != '\n');

			if (choice == 5) {
				printf("\nDATABASE SYSTEM END\n");
				break;
			}

			switch (choice) {
			case 1:
				printf("	1. SELECT\n");
				select();
				break;
			case 2:
				printf("	2. INSERT\n");
				insert();
				break;
			case 3:
				printf("	3. UPDATE\n");
				total = select();
				update(total);
				break;
			case 4:
				printf("	4. DELETE\n");
				total = select();
				delete(total);
				break;
			default:
				printf("\nENTER NUMBER BETWEEN 1~5\n");
				break;
			}
		}
	}

	save();
	printf("DATA SAVED !\n");

	system("pause");

	return 0;
}

void load(FILE* fp) {
	
	DATA *new_data;
	char input[50];
	char *name, *number;
	DATA *prev = NULL;

	while (!feof(fp)) {
		if (fgets(input, sizeof(input), fp) == NULL) 	break;

		new_data = (DATA*)malloc(sizeof(DATA));
		new_data->next = NULL;

		name = strtok(input, ",");
		number = strtok(NULL, "\n");
		
		strcpy(new_data->name, name);
		strcpy(new_data->number, number);
		new_data->check = 0;
		//printf("input : %s %s", new_data->name, new_data->number);
		if (head == NULL) { 
			head = new_data;
			prev = head;
		}
		else {
			DATA *tmp = prev;
			tmp->next = new_data;
			prev = tmp->next;
		}
	}
}
void save() {
	FILE *result = fopen("2017029552_남은성.csv", "w");

	DATA *tmp = head;
	while (tmp!= NULL) {
		fprintf(result, "%s,%s\n", tmp->name, tmp->number);
		tmp = tmp->next;
	}
}
int select() {

	char input[10];
	char search[38];
	int count = 0, mode;

	printf("SEARCH MODE: name OR number\n");
	gets(input);
	if (!strcmp(input, "name")) mode = 0;
	else if (!strcmp(input, "number")) mode = 1;
	else return;

	char *mode_c = (mode == 0) ? "name" : "number";

	printf("SEARCH %s mode : ", mode_c);
	gets(search);
	DATA *tmp = head;

	while (tmp != NULL) {
		tmp->check = 0;
		if ((mode == 0 && strstr(tmp->name, search)) || (mode == 1 && strstr(tmp->number, search))) {
			printf("%d. %s  %s\n", ++count, tmp->name, tmp->number);
			tmp->check = count;
		}
		tmp = tmp->next;
	}	
	printf("TOTAL : %d\n", count);

	return count;
}
void insert() {
	char name[50], number[12];

	printf("insert NAME : ");
	gets(name);
	printf("insert NUMBER : ");
	gets(number);

	DATA *new_data = (DATA*)malloc(sizeof(DATA));
	strcpy(new_data->name, name);
	strcpy(new_data->number,number);
	
	new_data->next = head->next;
	head ->next = new_data;

}
void update(int total) {

	if (total < 1) return;
	
	int confirm, mode;
	char input[50],find[50];
	DATA *tmp = head;

	printf("select one to update...(choose number): ");
	
	scanf("%d", &confirm);
	getchar();

	if (confirm > total) {
		printf("out of range\n");
		return;
	}

	while (tmp != NULL) {
		if (tmp->check == confirm) {
			printf("modify name %s (newname or just enter to skip): ",tmp->name);
			gets(input);
			if (input[0] != 0) {
				printf("update %s with %s....", tmp->name, input);
				strcpy(tmp->name, input);
			}
			printf("modify number %s (new number or just enter to skip): ",tmp->number);
			gets(find);
			if (find[0] != 0) {
				printf("update %s with %s....", tmp->number, find);
				strcpy(tmp->number, find);
			}
			return;
		}	
		tmp = tmp->next;
	}
}
void delete(int total) {

	if (total < 1) return;

	int confirm;
	char answer[40];
	DATA *de;

	printf("select one to delete...(choose number): ");
	scanf("%d", &confirm);
	getchar();

	if (confirm > total) {
		printf("out of range\n");
		return;
	}

	DATA* tmp = head;
	DATA* prev = NULL;
	while (tmp->check != confirm) {
		prev = tmp;
		tmp = tmp->next;
	}
	printf(" delete %s %s (yes OR no) ? : ", tmp->name, tmp->number);
	scanf("%s", answer);
	getchar();
	if (!strcmp(answer, "yes")) {
		de = tmp;
		prev->next = tmp->next;
		free(de);
		printf("DATA deleted\n");
		return;
	}
	else return;
}
