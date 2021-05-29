ajot = {"A005" "B005" "D005" "A002" "B002" "D002"};
alkuvuosi = 2006;
loppuvuosi = 2059;

kansio = '/home/aerkkila/a/pintaalat_15_1/';

for ajo = [1:length(ajot)]
  u = fopen([kansio 'pa_' ajot{ajo} '_maks.txt'], 'w');
  for vuosi=[alkuvuosi:loppuvuosi]
    tiedosto = [kansio 'pa_' ajot{ajo} '_' num2str(vuosi) '.bin'];
    f = fopen(tiedosto, 'r');
    alat = fread(f, [365 1], 'single');
    fclose(f);
    [m i] = max(alat);
    fprintf(u, "%.0f\t%i\t%i\n", m, i, vuosi);
  end
end
  
ajot = {"A001" "B001" "D001"};
alkuvuosi = 1975;
loppuvuosi = 2005;
  
for ajo = [1:length(ajot)]
  u = fopen([kansio 'pa_' ajot{ajo} '_maks.txt'], 'w');
  for vuosi=[alkuvuosi:loppuvuosi]
    tiedosto = [kansio 'pa_' ajot{ajo} '_' num2str(vuosi) '.bin'];
    f = fopen(tiedosto, 'r');
    alat = fread(f, [365 1], 'single');
    fclose(f);
    [m i] = max(alat);
    fprintf(u, "%.0f\t%i\t%i\n", m, i, vuosi);
  end
  fclose(u);
end
