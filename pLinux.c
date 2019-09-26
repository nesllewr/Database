#define _CRT_SECURE_NO_WARNINGS
#define MAX 1024

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

typedef struct DATA{
	char name[40];
	char number[15];
	int check;
	struct DATA *next;
}DATA;

DATA *head=NULL;

void load(FILE* fp);
void save();

int _select();
void insert();
void update(int total);
void delete(int total);

int main(int argc, char *argv[]) {

	int choice, total;
	char *ch = (char*)malloc(sizeof(char) * MAX);

	FILE *forigin = NULL;
	FILE *fp = NULL;
	char *file_name = "2017029552_남은성.csv";

	forigin = fopen("contact.csv", "r");


	if (access(file_name, 2) == 0) {
		printf("already copy contact.csv into %s\n", file_name);
		fp = fopen(file_name, "r");
	}//file_name이 있을 경우 이미 contact.csv파일이 학번_이름.csv파일로
	 //복사 되었다고 생각해서 read로 열어준다.
	else {
		if (forigin != NULL) {
			fp = fopen(file_name, "w+");
			printf("Data LOADING...\n");
			while ((fgets(ch, MAX, forigin)) != NULL) {
				fprintf(fp, "%s", ch);
			}//학번_이름.csv파일에 contact.csv파일을 fgets로 담아 온다.
		}
		free(ch);
	}

	fclose(forigin);

	rewind(fp); //데이터를 구조체에 넣기 위에 파일디스크립터를 처음으로 지정

	printf("DATA LOADING...");

	load(fp);
	fclose(fp); //데이터를 다 가지고 왔다면 데이터 파일은 닫아준다.
	
	
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
				_select();
				break;
			case 2:
				printf("	2. INSERT\n");
				insert();
				break;
			case 3:
				printf("	3. UPDATE\n");
				total = _select();
				update(total);
				break;
			case 4:
				printf("	4. DELETE\n");
				total = _select();
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

	//system("pause");

	return 0;
}

void load(FILE* fp) {
	
	DATA *new_data;
	char input[100];
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
		new_data->check = 0;//한 줄 씩 읽어온 데이터를 ","와 "\n"을 기준으로
                          //parsing한 다음 동적할당한 구조체에 넣어준다.
		//printf("input : %s %s", new_data->name, new_data->number);
		if (head == NULL) { 
			head = new_data;
			prev = head;//"name"과 "phone"은 head 구조체에 담아놓는다.
		}
		else {
			DATA *tmp = prev;
			tmp->next = new_data;
			prev = tmp->next;
		}//가장 마지막 노드를 prev에 저장해서 새로 받는 데이터를 뒤에 바로
	}   //연결하고 prev를 계속해서 update한다.
}
void save() {
	FILE *result = fopen("2017029552_남은성.csv", "w");

	DATA *tmp = head;
	while (tmp!= NULL) {
		fprintf(result, "%s,%s\n", tmp->name, tmp->number);
		tmp = tmp->next;
	} //학번_이름.csv파일을 write모드로 열어 DATA 구조체의 내용을
	// 개행문자와 함께 저장한다.
}
int _select() {

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
	scanf("%s",name);
	getchar();
	
	printf("insert NUMBER : ");
	scanf("%s",n);
	getchar();

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
