#include "../include/play_utils.h" 
#include "../include/utils.h"
#include "../include/print_utils.h"
#include "../include/ranking.h"
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <ctype.h>
#include <unistd.h>

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

void play(Player *ranking) {
	Player player;
	getPlayerName(player.name);

	const char WORDS_DATABASE_PATH[] = "src/words.txt";

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

	updateRanking(player, ranking);

	freeStrArray(&wordsList, wordsCount);
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