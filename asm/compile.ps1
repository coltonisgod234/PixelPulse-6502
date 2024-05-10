rm object.o -ErrorAction SilentlyContinue
rm out.bin -ErrorAction SilentlyContinue

ca65 source.s -o object.o --cpu 65C02
ld65 object.o -o out.bin -C conf/linker.cfg