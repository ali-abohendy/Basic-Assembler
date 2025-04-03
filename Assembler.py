PsudoOpcodes = ['ORG', 'END', 'DEC', 'HEX']

Memopcodes = {
    'AND': 0x0,
    'ADD': 0x1,
    'LDA': 0x2,
    'STA': 0x3,
    'BUN': 0x4,
    'BSA': 0x5,
    'ISZ': 0x6,
}

RegInstr = {
    'CLA': 0x7800,
    'CLE': 0x7400,
    'CMA': 0x7200,
    'CME': 0x7100,
    'CIR': 0x7080,
    'CIL': 0x7040,
    'INC': 0x7020,
    'SPA': 0x7010,
    'SNA': 0x7008,
    'SZA': 0x7004,
    'SZE': 0x7002,
    'HLT': 0x7001, 
}

InOutInstr = {
    'INP': 0xF800,
    'OUT': 0xF400,
    'SKI': 0xF200,
    'SKO': 0xF100,
    'ION': 0xF080,
    'IOF': 0xF040,
}
def parse_line(line):
    line = line.split('/')[0].strip()
    if not line:
        return None, None, None, False

    parts = line.split()
    label = None
    if parts[0].endswith(','):
        label = parts.pop(0)[:-1]

    opcode = parts.pop(0)
    indirect = False
    if parts and parts[-1] == 'I':
        indirect = True
        parts.pop()

    operand = parts[0] if parts else None

    return label, opcode, operand, indirect

def first_pass(lines):
    symbol_table = {}
    location_counter = 0

    for line in lines:
        label, opcode, operand, indirect = parse_line(line)
        if label:
            symbol_table[label] = location_counter

        if opcode in PsudoOpcodes:
            if opcode == 'ORG':
                location_counter = int(operand, 16)
            elif opcode == 'END':
                break
            else:
                location_counter += 1
        elif opcode in Memopcodes or opcode in RegInstr or opcode in InOutInstr:
            location_counter += 1
        else:
            print(f"Error: Invalid opcode {opcode}")

    return symbol_table

def second_pass(lines, symbol_table):
    machine_code = []
    location_counter = 0

    for line in lines:
        label, opcode, operand, indirect = parse_line(line)
        if not opcode:
            continue

        if opcode in PsudoOpcodes:
            if opcode == 'ORG':
                location_counter = int(operand, 16)
            elif opcode == 'END':
                break
            elif opcode == 'DEC':
                value = int(operand)
                if value < 0:
                    value = (1 << 16) + value
                machine_code.append(f"{location_counter:016b} {value:016b}")
                location_counter += 1
            elif opcode == 'HEX':
                value = int(operand, 16)
                if value < 0:
                    value = (1 << 16) + value
                machine_code.append(f"{location_counter:016b} {value:016b}")
                location_counter += 1
        elif opcode in Memopcodes:
            address = symbol_table.get(operand, 0)
            if address == 0:
                try:
                    address = int(operand, 16)
                except ValueError:
                    print(f"Error: Invalid operand {operand}")
                    continue
            if indirect:
                address |= 0x8000  # Set the indirect bit
            machine_code.append(f"{location_counter:016b} {Memopcodes[opcode] << 12 | address:016b}")
            location_counter += 1
        elif opcode in RegInstr:
            machine_code.append(f"{location_counter:016b} {RegInstr[opcode]:016b}")
            location_counter += 1
        elif opcode in InOutInstr:
            machine_code.append(f"{location_counter:016b} {InOutInstr[opcode]:016b}")
            location_counter += 1
        else:
            print(f"Error: Invalid opcode {opcode}")

    return machine_code

def assemble(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    symbol_table = first_pass(lines)
    machine_code = second_pass(lines, symbol_table)

    output_path = "Machine_Code.txt"
    with open(output_path, 'w') as file:
        for code in machine_code:
            file.write(code + '\n')

    print(f"Assembly complete. Output written to {output_path}")

if __name__ == "__main__":
    file_path = "asm.txt"
    assemble(file_path)
