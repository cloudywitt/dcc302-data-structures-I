#include <string.h>
#include "../include/utils.h"
#include "../include/ranking.h"
#define LOWEST_RANK 5

void insertOnRanking(Player player, Player *ranking, int position) {
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

void updateRanking(Player player, Player *ranking) {
	for (int i = 0; i < LOWEST_RANK; i++) {
		if (ranking[i].name == NULL || player.score > ranking[i].score) {
			insertOnRanking(player, ranking, i);

			break;
		}
	}
}