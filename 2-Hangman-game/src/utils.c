#include "../include/utils.h"
#include "../include/print_utils.h"
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

FILE *openFile(const char name[], const char * restrict mode) {
	FILE *filePtr = fopen(name, mode);

	if (filePtr == NULL) {
		printf("ERROR: Couldn't open %s\n", name);

		exit(1);
	}

	return filePtr;
}

int getOption() {
	int option;

	while (true) {
		printMenu();
		int scanfReturn = scanf("%d", &option);
		clearInputBuffer();

		// Option validation
		const bool isNotANumber = scanfReturn == 0;
		const bool isOutOfMenuRange = option < PLAY || option > EXIT;

		if (isNotANumber) {
			clearScreen();

			printf("ERROR: Enter a number.\n\n");
		} else if (isOutOfMenuRange) {
			clearScreen();

			printf("ERROR: Enter a valid option.\n\n");
		} else {
			break;
		}
	}

	return option;
}

void clearInputBuffer() {
	while (getchar() != '\n');
}

void clearScreen() {
	printf("\e[1;1H\e[2J");
}

void freeStrArray(char ***array, size_t size) {
	for (size_t i = 0; i < size; i++) {
		free((*array)[i]);
	}

	free(*array);
}