#define _CRT_SECURE_NO_WARNINGS

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

void select(FILE* fp);
void insert(FILE* fp);
void update(FILE* fp);
void delete(FILE* fp);

int main(int argc, char *argv[]) {

	int choice;
	int data_size = 0 ;

	FILE *fp = NULL;

	fp = fopen("contact2.csv", "a+");

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

			rewind(fp);
		}
	}

	fclose(fp);

	system("pause");

	return 0;
}


void select(FILE* fp) {
	
	char input[10], data[50];
	char find_name[38], find_number[12];
	char *name, *number;
	int count =0;

	printf("NAME ((((or NUMBER))))))))\n");
	scanf("%s", input);

	if (!strcmp(input, "NAME")) {
		printf("SEARCH: ");
		scanf("%s", find_name);
		while (!feof(fp)) {
			if (fgets(data, sizeof(data), fp) == NULL) break;

			name = strtok(data, ",");
			number = strtok(NULL, ",");

			if (strstr(name, find_name)) {
				printf("%s %s\n", name, number);
				count++;
			}
		}
		printf("total : %d\n", count);
	}
	else if(!strcmp(input, "NUMBER")) {
		printf("SEARCH: ");
		scanf("%s", find_number);
		while (!feof(fp)) {
			if (fgets(data, sizeof(data), fp) == NULL) break;

			name = strtok(data, ",");
			number = strtok(NULL, ",");

			if (strstr(number, find_number)) {
				printf("%s %s\n", name, number);
				count++;
			}
				
		}
		printf("total : %d\n", count);
	}
	else {
		printf("WRONG : BACK TO FUNCTION\n");
	}
}
void insert(FILE* fp) {

	//position = fseek(fp, 0, SEEK_END);

	//fputs("WRITE", fp);

	//fseek(fp, 0, SEEK_SET);

}
void update(FILE* fp) {

}
void delete(FILE* fp) {

	char input[10], data[50];
	char find_name[38], find_number[12];
	char *name, *number;
	long seek, start;

	printf("NAME or NUMBER\n");
	scanf("%s", input);

	if (!strcmp(input, "NAME")) {
		printf("SEARCH: ");
		scanf("%s", find_name);
		while (!feof(fp)) {
			if (fgets(data, sizeof(data), fp) == NULL) {
				printf("There is no such name in this database system.\n");
				break;
			}

			name = strtok(data, ",");
			number = strtok(NULL, ",");
			
			if (!strcmp(name, find_name)) {
				printf("deleting %s %s\n", name, number);
				seek = ftell(fp);
				start = seek;

				break;
			}
		}
	}
	else if (!strcmp(input, "NUMBER")) {
		printf("SEARCH: ");
		scanf("%s", find_number);
		while (!feof(fp)) {
			if (fgets(data, sizeof(data), fp) == NULL) {
				printf("There is no such name in this database system.\n");
				break;
			}
			name = strtok(data, ",");
			number = strtok(NULL, ",");

			if (!strcmp(number, find_number)) {
				printf("deleting %s %s\n", name, number);
			}

		}
	}


}
