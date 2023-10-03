#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> 
#include <ctype.h> 
#include <time.h>
#include <stdbool.h>
#include <string.h>

#include "../include/utils.h"
#include "../include/print_utils.h"
#include "../include/ranking.h"
#include "../include/play_utils.h"

#define MAX_NAME_SIZE 30
#define MENU_OPTIONS_QUANTITY 3
#define LOWEST_RANK 5

int main() {
	Player ranking[5];

	srand(time(NULL));
	clearScreen();

	while (true) {
		int option = getOption();
		
		if (option == PLAY) {
			play(ranking);
		} else if (option == RANKING) {
			printRanking(ranking);
		} else if (option == EXIT) {
			printf("Thanks for playing! Exiting the game...\n");

			break;
		}
	}

	return 0;
}
