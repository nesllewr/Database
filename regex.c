#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
	char *input = "01012341234";

	regex(input);
	// char result1[100];
	// char base[100];

	// sscanf(input1, "%3[0-9]%8[0-9]", base, result1);

	// int check = 1;
	// if(!strcmp(base, "010")) {
	// 	strcat(base, result1);
	// 	if(strcmp(base, input1)) {
	// 		check = 0; 
	// 	}
	// } else {
	// 	check = 0;
	// }

	// if(check == 0) {
	// 	printf("%s and %s is incorrect\n", input1, base);
	// } else {
	// 	printf("%s and %s is correct\n", input1, base);
	// }

	return 0;
}
//inputdl 뜰어온거 
int regex(char *input){

	char result[100];
	char base[100];

	sscanf(input, "%3[0-9]%8[0-9]", base, result);
	

	int check = 1;
	if(!strcmp(base, "010")) {
		strcat(base, result);
		if(!strcmp(base, input)) {
			check = 0; 
		}
	} else {
		check = 1;
	}

	if(check == 1) {
		printf("%s and %s is incorrect\n", input, base);
	} else {
		printf("%s and %s is correct\n", input, base);
	}

	return check;


}

