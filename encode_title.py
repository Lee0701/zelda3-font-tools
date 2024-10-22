import sys

def read_hex_csv(content):
    lines = content.split('\n')
    lines = [line.strip() for line in lines if line]
    lines = [line.split(',') for line in lines]
    lines = [[int(cell, 16) for cell in line] for line in lines]
    return lines

def flush(result, addr, out):
    if len(out) == 0:
        return addr + 1
    result.append(0x11)
    result.append(addr)
    result.append(0x00)
    result.append(len(out) * 2 - 1)
    for v in out:
        result.append(v)
        result.append(0x39)
        addr += 1
    out.clear()
    return addr + 1

def encode_tile(content):
    result = []
    out = []
    content = read_hex_csv(content)
    for j, line in enumerate(content):
        addr = 0x25 + j * 0x20
        for cell in line:
            if cell == 0x0c:
                addr = flush(result, addr, out)
            else:
                out.append(cell)
        addr = flush(result, addr, out)
    return result

def main(args):
    input, output = args
    with open(input, 'r') as file:
        content = file.read()
    content = encode_tile(content)
    with open(output, 'wb') as file:
        file.write(bytearray(content))
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
