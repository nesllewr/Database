#define _CRT_SECURE_NO_WARNINGS
#define MAX 1024

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <io.h>

typedef struct {
	char name[40];
	char number[12];
	struct DATA *next;
}DATA;

DATA *head = NULL;

void load(FILE* fp);
void select();
void insert();
void update();
void delete();


int main(int argc, char *argv[]) {

	int choice;
	char *ch = (char*)malloc(sizeof(char) * MAX);

	FILE *forigin = NULL;
	FILE *fp = NULL;
	char *file_name = "pr.csv";

	forigin = fopen("contact2.csv", "r");

	if (_access(file_name, 2) == 0) {
		printf("already copy contact.csv into %s\n", file_name);
		fp = fopen("pr.csv", "w+");
	}
	else {
		if (forigin != NULL) {
			fp = fopen(file_name, "w+");
			printf("Data LOADING...\n");
			while ((fgets(ch, MAX, forigin)) != NULL) {
				fprintf(fp, "%s", ch);
				printf("%s", ch);
			}
		}
		free(ch);
	}

	fclose(forigin);
	printf("before load\n");

	rewind(fp);
	/*int i = 0;
	while ((fgets(ch, MAX, fp)) != NULL) {
		//fprintf(fp, "%s", ch);
		printf("%d %s", i++, ch);
	}*/

	load(fp);

	printf("after load");
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
				update();
				break;
			case 4:
				printf("	4. DELETE\n");
				delete();
				break;
			default:
				printf("\nENTER NUMBER BETWEEN 1~5\n");
			}
		}
	}

	fclose(fp);

	system("pause");

	return 0;
}

void load(FILE* fp) {
	DATA *new_data;
	while (!feof(fp)) {
		new_data = (DATA*)malloc(sizeof(DATA));
		new_data->next = NULL;
		fscanf(fp, "%s,%d", &new_data->name, &new_data->number);

		if (head == NULL) head = new_data;
		else {
			DATA *tmp = head;
			while (tmp->next != NULL) {
				tmp = tmp->next;
			}
			tmp->next = new_data;
		}
	}
}


void select() {

	char input[10];
	char search[38];
	char *name, *number;
	int count = 0, i=0, mode;

	printf("name OR number\n");
	scanf("%s", input);

	if (!strcmp(input, "name")) mode = 0;
	else if (!strcmp(input, "number")) mode = 1;
	else return;

	char *mode_c = (mode == 0) ? "name" : "number";

	printf(" %s mode SEARCH: ", mode_c);
	scanf("%s", search);

	/*while ( i < data_count) {
		if ((mode == 0 && strstr(data[i].name, search)) || (mode == 1 && strstr(data[i].number, search))) {
			printf("%s %s\n", data[i].name, data[i].number);
			count++;
		}
		i++;
	}*/
	printf("total : %d\n", count);
}
void insert() {
}
void update() {
}
void delete() {

}