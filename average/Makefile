CC = gcc
ASM = nasm
ASMFLAGS = -f elf64
CFLAGS = -no-pie
TARGET = average

all: $(TARGET)

$(TARGET): main.o
	$(CC) $(CFLAGS) -o $(TARGET) main.o

main.o: main.asm
	$(ASM) $(ASMFLAGS) main.asm -o main.o

run: $(TARGET)
	./$(TARGET) data.txt

clean:
	rm -f $(TARGET) main.o

.PHONY: all run clean
