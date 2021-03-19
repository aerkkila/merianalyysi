paksuudet:
	gcc -o paksuudet.out paksuudet.c -O3

laske:	paksuudet
	./paksuudet.out icevolume_ A001 B001 D001 1975 2005
	./paksuudet.out icevolume_ A002 A005 B002 B005 D002 D005 2006 2059
	./paksuudet.out soicecov_ A001 B001 D001 1975 2005
	./paksuudet.out soicecov_ A002 A005 B002 B005 D002 D005 2006 2059

maksimit: paksuudetmaks
	./paksuudetmaks.out

paksuudetmaks:
	gcc -g -o paksuudetmaks.out paksuudetmaks.c -O0

ajankohdat:
	gcc -g -o ajankohdat.out ajankohdat.c
