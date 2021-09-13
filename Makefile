pintaalat: pintaalat.c
	gcc -g -Wall pintaalat.c -std=gnu99 -lnetcdf -lhdf5 -lm

paksuudet: paksuudet.c
	gcc -g -Wall paksuudet.c -std=gnu99 -lnetcdf -lhdf5 -lm

paksuudet3: paksuudet.c
	gcc -g -Wall paksuudet.c -std=gnu99 -lnetcdf -lhdf5 -lm -O3
