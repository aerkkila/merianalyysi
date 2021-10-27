#ifdef TULEVA
#define PAIKKOJA 6
const char* nimitunniste = "";
char* paikat[] = {"Kemi", "Kalajoki", "Mustasaari", "Nordmaling", "Rauma", "Söderhamn"};
char* paikat_en[] = {"Kemi", "Kalajoki", "Korsholm", "Nordmaling", "Rauma", "Söderhamn"};
float paikatlat[] = {65.6322, 64.2250, 63.1579, 63.4498, 61.1050, 61.3897};
float paikatlon[] = {24.4908, 23.6921, 21.2553, 19.6341, 21.4220, 17.1539};
#endif
#ifdef HISTORIA
#define PAIKKOJA 9
const char* nimitunniste = "_hist";
char* paikat[] = {"Tornio", "Kemi", "Hailuoto", "Raahe", "Bygdeå", "Nordmaling", "Kalajoki", "Kokkola", "Mustasaari"};
char* paikat_en[] = {"Tornio", "Kemi", "Hailuoto", "Raahe", "Bygdeå", "Nordmaling", "Kalajoki", "Kokkola", "Korsholm"};
float paikatlat[] = {65.7658, 65.6322, 65.0435, 64.6499, 63.9817, 63.4498, 64.2250, 63.8896, 63.4400};
float paikatlon[] = {24.2124, 24.4908, 24.5516, 24.3863, 20.8990, 19.6341, 23.6921, 22.9450, 21.0548};
#endif
