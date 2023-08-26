#include <stdio.h>
#include <stdlib.h>
#include <unistd.h> // sleep()
#include <ctype.h> // tolower()
#include <time.h> // time()
#include <stdbool.h>
#include <string.h>
#define MAX_NAME_SIZE 30
#define MENU_OPTIONS_QUANTITY 3
#define LOWEST_RANK 5

typedef struct {
	char name[MAX_NAME_SIZE];
	int score;
} Player;

Player ranking[5];

enum Options {
	PLAY = 1,
	RANKING,
	EXIT,
};

FILE *openFile(const char name[], const char * restrict mode) {
	FILE *filePtr = fopen(name, mode);

	if (filePtr == NULL) {
		printf("ERROR: Couldn't open %s\n", name);

		exit(1);
	}

	return filePtr;
}

void freeStrArray(char ***array, size_t size) {
	for (size_t i = 0; i < size; i++) {
		free((*array)[i]);
	}

	free(*array);
}

void clearInputBuffer() {
	while (getchar() != '\n');
}

void clearScreen() {
	printf("\e[1;1H\e[2J");
}

void printMenu() { 
	printf("## The C Hangman Game ##\n");
	printf("[1] PLAY\n");
	printf("[2] RANKING\n");
	printf("[3] EXIT\n");
	printf("Enter an option: ");
}

void printRanking() {
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

void getPlayerName(char pname[]) {
	clearScreen();

	printf("\n-- Sign Up --\n\n");
	printf("Enter your name: ");
	fgets(pname, MAX_NAME_SIZE, stdin);

	int nameLen = strlen(pname);

	if (nameLen == MAX_NAME_SIZE) {
		pname[nameLen - 1] = '\0';
	} else {
		pname[strcspn(pname, "\n")] = '\0';
	}

	clearScreen();
}

void loadWords(const char filePath[], char ***wordsArrayPtr, size_t *wordsQuantity) {
	FILE *wordsFilePtr = openFile(filePath, "r");

	size_t maxCapacity = 10;
	*wordsArrayPtr = malloc(maxCapacity * sizeof(char*));

	char buffer[256];
	size_t wordsCount = 0;

	// Read every word in file
	while (fgets(buffer, sizeof(buffer), wordsFilePtr) != NULL) {
		// Checks capacity
		if (wordsCount >= maxCapacity) {
			maxCapacity *= 2;

			*wordsArrayPtr = realloc(*wordsArrayPtr, maxCapacity * sizeof(char*));
		}

		// Replace \n by \0
		buffer[strcspn(buffer, "\n")] = '\0'; // Hint: not secure for when the word is bigger than 256

		// Allocates memory for the word
		(*wordsArrayPtr)[wordsCount] = malloc(strlen(buffer) + 1);

		// Copies the word to the array
		strcpy((*wordsArrayPtr)[wordsCount], buffer);
		
		wordsCount++;
	}

	// Removes not used array space
	*wordsArrayPtr = realloc(*wordsArrayPtr, wordsCount * sizeof(char*));

	// Sets array size
	*wordsQuantity = wordsCount;

	fclose(wordsFilePtr);
}

// Game Functions
char *pickRandomWord(char **wordsArray, size_t wordsQuantity) {
	int wordIndex = random() % wordsQuantity;
	char *pickedWord = NULL;

	for (int i = 0; i < wordsQuantity; i++) {
		if (wordsArray[wordIndex] != NULL) {
			pickedWord = wordsArray[wordIndex];

			wordsArray[wordIndex] = NULL;

			break;
		}

		int nextIndex = (wordIndex + 1) % wordsQuantity;
		wordIndex = nextIndex;
	}

	return pickedWord;
}

char *hideWord(const char word[]) {
	size_t wordLen = strlen(word);
	char *hiddenWord = malloc(wordLen + 1);

	for (size_t i = 0; i < wordLen; i++) {
		hiddenWord[i] = (word[i] != ' ') ? '-': ' ';
	}

	hiddenWord[wordLen] = '\0';

	return hiddenWord;
}

void updateHiddenWord(const char *secretWord, char *hiddenWord, char letter) {
    const size_t wordLen = strlen(secretWord);

    for (int i = 0; i < wordLen; i++) {
        if (tolower(letter) == tolower(secretWord[i]) ) {
            hiddenWord[i] = secretWord[i];
    	}
	}
}

bool playGuessWord(const char playerName[], const char secretWord[], int wordsGuessed, int wordsTotal) {
	char *secretWordHided = hideWord(secretWord);
	int lives = 6;
	bool gameOver = false;

	while (true) {
		clearScreen();

		printf("### HANGMAN GAME ### \t Word: %d/%d\n", wordsGuessed, wordsTotal);
		printHangman(lives);
		printf("## PLAYER: [%s] ##\n", playerName);
		printf("The word: %s\n", secretWordHided);

		printf("Enter a letter: ");
		char guessedLetter = getchar();
		clearInputBuffer();
		printf("The letter: %c\n", guessedLetter);

		// Check answer
		bool letterIsInWord = false;
        for (int i = 0; secretWord[i] != '\0'; i++) {
            if (guessedLetter == secretWord[i] || tolower(guessedLetter) == tolower(secretWord[i])) {
                letterIsInWord = true;
                updateHiddenWord(secretWord, secretWordHided, secretWord[i]);
            }
        }

        if (!letterIsInWord) {
            lives--;
        }

		// check win and lose conditions
		bool playerGuessedWord = strcmp(secretWord, secretWordHided) == 0;
		bool playerLose = lives == 0;
		
		if (playerGuessedWord) {
			clearScreen();
			printf("You win! The word was: %s\n", secretWord);
			sleep(2);

			break;
		} else if (playerLose) {
			clearScreen();
			printHangman(lives);
			printf("You lose! The word was: %s\n", secretWord);

			gameOver = true;

			break;
		}
	}

	free(secretWordHided);

	return gameOver;
}

void insertOnRanking(Player player, int position) {
	if (ranking[position].name == NULL) {
		strcpy(ranking[position].name, player.name);
        ranking[position].score = player.score;

		return;
	}

	for (int i = LOWEST_RANK - 1; i >= position; i--) {
        ranking[i] = ranking[i - 1];
	}
 
	strcpy(ranking[position].name, player.name);
    ranking[position].score = player.score;
}

void updateRanking(Player player) {
	for (int i = 0; i < LOWEST_RANK; i++) {
		if (ranking[i].name == NULL || player.score > ranking[i].score) {
			insertOnRanking(player, i);

			break;
		}
	}
}

void play() {
	Player player;
	getPlayerName(player.name);

	const char WORDS_DATABASE_PATH[] = "words.txt";
	char **wordsList;
	size_t wordsCount;
	loadWords(WORDS_DATABASE_PATH, &wordsList, &wordsCount);

	int wordsGuessed = 0;

	while (wordsGuessed < wordsCount) {
		char *secretWord = pickRandomWord(wordsList, wordsCount);

		bool gameOver = playGuessWord(player.name, secretWord, wordsGuessed, wordsCount);

		if (gameOver == true) {
			break;
		}

		wordsGuessed++;
	}

	player.score = wordsGuessed * 100;

	printf("Your score is %d\n", player.score);
	sleep(2);
	clearScreen();

	updateRanking(player);

	freeStrArray(&wordsList, wordsCount);
}

int main() {
	srand(time(NULL));
	clearScreen();

	while (true) {
		int option = getOption();
		
		if (option == PLAY) {
			play();
		} else if (option == RANKING) {
			printRanking();
		} else if (option == EXIT) {
			printf("Thanks for playing! Exiting the game...\n");

			break;
		}
	}

	return 0;
}
