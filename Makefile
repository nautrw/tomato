CC=gcc
PKG=libadwaita-1
TARGET=tomato
OBJS=main.o

CFLAGS=-Wall -Wextra -Werror -std=c11 -O2 \
	   $(shell pkg-config --cflags $(PKG))

LDLIBS=$(shell pkg-config --libs $(PKG))

$(TARGET): $(OBJS)
	$(CC) $(OBJS) -o $(TARGET)

%.d: %.c
	$(CC) -MM $(CFLAGS) $< -o $@
-include $(OBJS:.o=.d)

flags:
	echo "$(CFLAGS)"

.PHONY: clean
clean:
	rm -f *.o *.d *.out $(TARGET)

