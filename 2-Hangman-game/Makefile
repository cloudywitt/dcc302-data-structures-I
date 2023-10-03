hangman: main.o utils.o print_utils.o ranking.o play_utils.o
	gcc obj/main.o obj/utils.o obj/print_utils.o obj/ranking.o obj/play_utils.o -o bin/hangman

main.o: src/main.c
	gcc -c src/main.c -o obj/main.o

utils.o: src/utils.c include/utils.h
	gcc -c src/utils.c -o obj/utils.o

print_utils.o: src/print_utils.c include/print_utils.h
	gcc -c src/print_utils.c -o obj/print_utils.o

ranking.o: src/ranking.c include/ranking.h
	gcc -c src/ranking.c -o obj/ranking.o

play_utils.o: src/play_utils.c include/play_utils.h
	gcc -c src/play_utils.c -o obj/play_utils.o 

clean:
	rm obj/*.o bin/hangman