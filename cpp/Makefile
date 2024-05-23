CXX = g++
CXXFLAGS = -Wall -Wextra -std=c++17 -I/usr/local/include/
LDFLAGS = -lrf24

SOURCES = $(wildcard *.cpp)

OBJECTS = $(SOURCES:.cpp=.o)

TARGET = node

all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CXX) -o $@ $^ $(LDFLAGS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c -o $@ $<

clean:
	rm -f $(OBJECTS) $(TARGET)

.PHONY: all clean


