# Assembler for Custom Machine Instructions

This repository contains a Python-based assembler that translates a custom assembly language into machine code. The assembler processes an assembly source file (`asm.txt`) and generates a machine code output file (`Machine_Code.txt`).

## Features

- Supports pseudo-opcodes (`ORG`, `END`, `DEC`, `HEX`).
- Handles memory-reference, register, and I/O instructions.
- Implements a two-pass assembly process:
  1. **First pass**: Builds the symbol table.
  2. **Second pass**: Generates the machine code.

## Usage

1. Place your assembly instructions in `asm.txt`.
2. Run the assembler using:
   ```bash
   python Assembler.py
   ```
3. The output will be saved in `Machine_Code.txt`.

## Example

### Input (`asm.txt`):

```
ORG 100
LDA VALUE
ADD TEMP
STA RESULT
HLT
VALUE, DEC 5
TEMP, DEC 10
RESULT, HEX 0
END
```

### Output (`Machine_Code.txt`):

```
0000000000010000 0000001000000110
0000000000010001 0000000100000111
0000000000010010 0000001100001000
0000000000010011 0111000000000001
0000000000010100 0000000000000101
0000000000010101 0000000000001010
0000000000010110 0000000000000000
```

## License

This project is open-source under the MIT License.
