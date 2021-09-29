pintaalat: pintaalat.c
	gcc -g -Wall pintaalat.c -std=gnu99 -lnetcdf -lhdf5 -lm

paksuudet0: paksuudet.c
	gcc -g -Wall paksuudet.c -std=gnu99 -lnetcdf -lhdf5 -lm

paksuudet: paksuudet.c
	gcc -g -Wall paksuudet.c -std=gnu99 -lnetcdf -lhdf5 -lm -O3

peittävyydet: peittävyydet.c
	gcc -g -Wall peittävyydet.c -std=gnu99 -lnetcdf -lhdf5 -lm -O3

makspaksuudet: makspaksuudet.c
	gcc -Wall makspaksuudet.c -O3

pituus: pituus.c
	gcc -Wall pituus.c -O3

esiintyvyys: esiintyvyys.c
	gcc -shared -o esiintyvyys.so esiintyvyys.c -lm -O3 -Wno-unused-result

esiintyvyys_saadettava: esiintyvyys_säädettävä.c
	gcc -g -shared -o esiintyvyys_säädettävä.so esiintyvyys_säädettävä.c -lm -O3 -Wno-unused-result
