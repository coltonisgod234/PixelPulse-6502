"""
Disk spec:

| Byte | Purpose                  |
|------|--------------------------|
| 0x00 | Command
| 0x01 | Data
| 0x02 | Cylinder
| 0x03 | Head
| 0x04 | Sector


| Command |
|---------|
| READB   |
| WRITEB  |
| READSEC |
"""

CMD_REG = 0x00
DATA_REG = 0x01
CYL_REG = 0x02
HEAD_REG = 0x03
SECTOR_REG = 0x04
BYTE_LO_REG = 0x05
BYTE_HI_REG = 0x06

HEADS_PER_DISK = 2
SECTORS_PER_TRACK = 18
BYTES_PER_SECTOR = 512

class Diskette:
    def __init__(self, file) -> None:
        self.filepath = file
        self.fp = open(self.filepath, "wb")

    def get_offset(self, c:int, h:int, s:int, b:int) -> int:
        # Calculate the offset
        offset = ((c * HEADS_PER_DISK + h) * SECTORS_PER_TRACK * BYTES_PER_SECTOR) + ((s - 1) * BYTES_PER_SECTOR) + b
        
        return offset
    
    def write(self, c:int, h:int, s:int, b:int, data:int) -> None:
        with self.fp as fp:
            offset = self.get_offset(c, h, s, b)
            fp.seek(offset, 0)
            fp.write(data)

    def read(self, c:int, h:int, s:int, b:int) -> int:
        with self.fp as fp:
            offset = self.get_offset(c, h, s, b)
            fp.seek(offset, 0)
            data = fp.read(1)

        return data
    
    def change(self, new_file) -> None:
        self.filepath = new_file
        self.fp = open(self.filepath, "wb")

def tick_disks(cpu):
    disk_ram = cpu.memory[0x3030:0x303f]
    command = disk_ram[CMD_REG]