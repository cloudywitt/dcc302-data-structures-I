/* 
1) Refaça as funções de busca sequencial e busca binária discutidas em aula, assumindo que a
lista possui chaves que podem ocorrer múltiplas vezes na lista. Neste caso, você deve retornar
uma lista com todas as posições onde a chave foi encontrada. Se a chave não for encontrada na
lista, retornar uma lista vazia. Entrada consiste numa lista de inteiros com itens repetidos e
um item qualquer que esteja se repetindo.

Entrada (lista, item)                               Saída
[2, 2, 5, 8, 23, 24, 32, 44, 56, 99], 2             [0,1]
[1, 13, 21, 21, 21, 25, 36, 74], 21                 [2, 3, 4]
[4, 14, 15, 19, 21, 23, 45, 78, 81, 81, 90], 81     [8, 9]
[2, 2, 5, 8, 23, 24, 32, 44, 56, 99], 7             [ ]
*/
#include <stdio.h>
#include <stdlib.h>
#define END_OF_ARRAY -1

int *linearSearch(int array[], size_t size, int target) {
    int *targetPositions = malloc(sizeof(int));
    int targetOccurrencesCount = 0;

    for (size_t i = 0; i < size; i++) {
        if (target == array[i]) {
            targetPositions[targetOccurrencesCount] = i;
            targetOccurrencesCount++;

            targetPositions = realloc(targetPositions, sizeof(int) * (targetOccurrencesCount + 1));
        }
    }

    targetPositions[targetOccurrencesCount] = END_OF_ARRAY;

    return targetPositions;
}

int findFirstOccurrence(int array[], size_t size, int target) {
    int low = 0;
    int high = size - 1;
    int result = -1;

    while (low <= high) {
        int mid = (low + high) / 2;

        if (target == array[mid]) {
            result = mid;
            high = mid - 1;
        } else if (target < array[mid]) {
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }

    return result;
}

int findLastOccurrence(int array[], size_t size, int target) {
    int low = 0;
    int high = size - 1;
    int result = -1;

    while (low <= high) {
        int mid = (low + high) / 2;

        if (target == array[mid]) {
            result = mid;
            low = mid + 1;
        } else if (target < array[mid]) {
            high = mid - 1;
        } else {
            low = mid + 1;
        }
    }

    return result;
}

int *binarySearch(int array[], size_t size, int target) {
    int start = findFirstOccurrence(array, size, target);
    int end = findLastOccurrence(array, size, target);

    if (start == -1) {
        start = 0;
    }

    size_t targetOccurrencesCount = end - start + 1;

    int *targetPositions = malloc(sizeof(int) * (targetOccurrencesCount + 1));
    
    for (int i = start, j = 0; i <= end; i++, j++) {
        targetPositions[j] = i;
    }

    targetPositions[targetOccurrencesCount] = END_OF_ARRAY;

    return targetPositions;
}

void printHeapArray(int array[]) {
    int i = 0;

    printf("[ ");
    while (array[i] != END_OF_ARRAY) {
        printf("%d ", array[i]);

        i++;
    }

    printf("]\n");
}

int main() {
    // Case 1: [2, 2, 5, 8, 23, 24, 32, 44, 56, 99], 2             // Output: [0, 1]
    int numbers[] = {2, 2, 5, 8, 23, 24, 32, 44, 56, 99};
    const size_t numbersSize = sizeof(numbers) / sizeof(numbers[0]);
    int target = 2;

    int *positionsOfTarget = binarySearch(numbers, numbersSize, target);

    printHeapArray(positionsOfTarget);

    free(positionsOfTarget);

    return 0;
}