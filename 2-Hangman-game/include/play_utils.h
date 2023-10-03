#ifndef PLAY_UTILS_H
#define PLAY_UTILS_H
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include "utils.h"

void loadWords(const char filePath[], char ***wordsArrayPtr, size_t *wordsQuantity);

char *pickRandomWord(char **wordsArray, size_t wordsQuantity);

char *hideWord(const char word[]);

void updateHiddenWord(const char *secretWord, char *hiddenWord, char letter);

void play(Player *ranking);

bool playGuessWord(const char playerName[], const char secretWord[], int wordsGuessed, int wordsTotal);

void getPlayerName(char pname[]);

#endif