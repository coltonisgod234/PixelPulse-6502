rm object.o -ErrorAction SilentlyContinue
rm out.bin -ErrorAction SilentlyContinue

ca65 source.s -o object.o
ld65 object.o -o out.bin -C linker.cfg