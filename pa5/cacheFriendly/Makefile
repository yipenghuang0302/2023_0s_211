OUTPUT=matMul
CFLAGS=-O3 -floop-nest-optimize -Wall -Werror -std=c99
# -O3 -floop-nest-optimize
# -fsanitize=address
# -floop-interchange
# -floop-nest-optimize
LFLAGS=-lm

%: %.c %.h
	gcc $(CFLAGS) -o $@ $< $(LFLAGS)

%: %.c
	gcc $(CFLAGS) -o $@ $< $(LFLAGS)

all: $(OUTPUT)

clean:
	rm -f *.o $(OUTPUT)
