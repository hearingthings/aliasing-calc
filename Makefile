# Makefile for Aliasing Calculator C Implementation

CC = gcc
CFLAGS = -Wall -Wextra -O2 -std=c99
LDFLAGS = -lm

# Directories
SRC_DIR = c_impl
EXAMPLES_DIR = examples_c
BUILD_DIR = build

# Source files
LIB_SRC = $(SRC_DIR)/aliasing_calc.c
LIB_OBJ = $(BUILD_DIR)/aliasing_calc.o

# Examples
EXAMPLES = basic_example subharmonic_example realtime_example
EXAMPLE_BINS = $(addprefix $(BUILD_DIR)/, $(EXAMPLES))

# Targets
.PHONY: all clean examples lib

all: lib examples

# Create build directory
$(BUILD_DIR):
	mkdir -p $(BUILD_DIR)

# Build library object
lib: $(BUILD_DIR) $(LIB_OBJ)

$(LIB_OBJ): $(LIB_SRC) $(SRC_DIR)/aliasing_calc.h
	$(CC) $(CFLAGS) -c $(LIB_SRC) -o $(LIB_OBJ)

# Build examples
examples: $(EXAMPLE_BINS)

$(BUILD_DIR)/basic_example: $(EXAMPLES_DIR)/basic_example.c $(LIB_OBJ)
	$(CC) $(CFLAGS) $< $(LIB_OBJ) $(LDFLAGS) -o $@

$(BUILD_DIR)/subharmonic_example: $(EXAMPLES_DIR)/subharmonic_example.c $(LIB_OBJ)
	$(CC) $(CFLAGS) $< $(LIB_OBJ) $(LDFLAGS) -o $@

$(BUILD_DIR)/realtime_example: $(EXAMPLES_DIR)/realtime_example.c $(LIB_OBJ)
	$(CC) $(CFLAGS) $< $(LIB_OBJ) $(LDFLAGS) -o $@

# Run examples
run-basic: $(BUILD_DIR)/basic_example
	@echo "Running basic example..."
	@./$(BUILD_DIR)/basic_example

run-subharmonic: $(BUILD_DIR)/subharmonic_example
	@echo "Running subharmonic example..."
	@./$(BUILD_DIR)/subharmonic_example

run-realtime: $(BUILD_DIR)/realtime_example
	@echo "Running realtime example..."
	@./$(BUILD_DIR)/realtime_example

run-all: run-basic run-subharmonic run-realtime

# Clean build artifacts
clean:
	rm -rf $(BUILD_DIR)

# Help
help:
	@echo "Aliasing Calculator C Implementation - Makefile"
	@echo ""
	@echo "Targets:"
	@echo "  all              - Build library and all examples (default)"
	@echo "  lib              - Build library object file"
	@echo "  examples         - Build all example programs"
	@echo "  clean            - Remove build artifacts"
	@echo ""
	@echo "  run-basic        - Run basic example"
	@echo "  run-subharmonic  - Run subharmonic example"
	@echo "  run-realtime     - Run realtime example"
	@echo "  run-all          - Run all examples"
	@echo ""
	@echo "Examples:"
	@echo "  make              # Build everything"
	@echo "  make run-all      # Build and run all examples"
	@echo "  make clean        # Clean build directory"
