@title Compiling...
ca65 ../asm/source.s -o ../asm/object.o --cpu 65C02
@title Linking...
ld65 ../asm/object.o -C ../asm/conf/linker.cfg -o ../asm/out.bin
@title pixelpulse_dbg: RUNNING
python3 main.py ../asm/out.bin

@pause