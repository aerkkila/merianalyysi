pintaalat: pintaalat.c
	gcc -g -Wall pintaalat.c -std=gnu99 -lnetcdf -lhdf5 -lm

tilavuudet0: paksuudet.c
	gcc -g -Wall paksuudet.c -std=gnu99 -lnetcdf -lhdf5 -lm -D MUUTTUJA=icevolume -D ULOSNIMIALKU=tilavuudet

tilavuudet: paksuudet.c
	gcc -g -Wall paksuudet.c -std=gnu99 -lnetcdf -lhdf5 -lm -O3 -D MUUTTUJA=icevolume -D ULOSNIMIALKU=tilavuudet

paksuudet: paksuudet.c
	gcc -g -Wall paksuudet.c -std=gnu99 -lnetcdf -lhdf5 -lm -O3 -D MUUTTUJA=icethic -D ULOSNIMIALKU=paksuudet

peittävyydet: peittävyydet.c
	gcc -g -Wall peittävyydet.c -std=gnu99 -lnetcdf -lhdf5 -lm -O3

paikat_kartalla: paikat_kartalla.c
	gcc -g -Wall paikat_kartalla.c -o paikat_kartalla -std=gnu99 -lnetcdf -lhdf5 -lm -O3
