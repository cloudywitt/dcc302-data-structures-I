#include "../include/utils.h"
#include "../include/print_utils.h"
#include <stdio.h>
#define LOWEST_RANK 5

void printMenu() { 
	printf("## The C Hangman Game ##\n");
	printf("[1] PLAY\n");
	printf("[2] RANKING\n");
	printf("[3] EXIT\n");
	printf("Enter an option: ");
}

void printRanking(Player *ranking) {
	clearScreen();
	printf("---- RANKING ----\n");

	for (int i = 0; i < LOWEST_RANK; i++) {
		printf("%d - %-10s \t Pts: %3d\n", i + 1, ranking[i].name, ranking[i].score);
	}

	printf("-------------------------\n");
}

void printHangman(int lives) {
	switch (lives) {
		case 6:
			printf("----------\n");
			printf("| \t |\n");
			printf("| \t \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("-\n");

			break;

		case 5:
			printf("----------\n");
			printf("| \t |\n");
			printf("| \t o\n");
			printf("| \t \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("-\n");

			break;
		case 4:
			printf("----------\n");
			printf("| \t |\n");
			printf("| \t o\n");
			printf("| \t |\n");
			printf("| \t \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("-\n");
		
			break;
		case 3:
			printf("----------\n");
			printf("| \t |\n");
			printf("| \t o\n");
			printf("| \t/|\n");
			printf("| \t \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("-\n");

			break;
		case 2:
			printf("----------\n");
			printf("| \t |\n");
			printf("| \t o\n");
			printf("| \t/|\\ \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("-\n");

			break;

		case 1:
			printf("----------\n");
			printf("| \t |\n");
			printf("| \t o\n");
			printf("| \t/|\\ \n");
			printf("| \t/ \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("-\n");

			break;

		case 0:
			printf("----------\n");
			printf("| \t |\n");
			printf("| \t o\n");
			printf("| \t/|\\ \n");
			printf("| \t/ \\ \n");
			printf("| \t \n");
			printf("| \t \n");
			printf("-\n");

			break;
	}
}
