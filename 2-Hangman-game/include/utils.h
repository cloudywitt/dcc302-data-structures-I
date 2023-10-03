#ifndef UTILS_H
#define UTILS_H
#include <stdio.h>
#include <stdlib.h>
#define MAX_NAME_SIZE 30

typedef struct {
	char name[MAX_NAME_SIZE];
	int score;
} Player;

enum Options {
	PLAY = 1,
	RANKING,
	EXIT,
};

FILE *openFile(const char name[], const char * restrict mode);

void clearInputBuffer();

void clearScreen();

void freeStrArray(char ***array, size_t size);

int getOption();

#endif