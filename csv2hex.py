import sys

def csv2hex(content):
    lines = content.split('\n')
    lines = [line.strip() for line in lines if line]
    hex_lines = []
    for line in lines:
        line = line.split(',')
        hex_line = []
        for cell in line:
            cell = cell.strip()
            cell = int(cell)
            cell = f'{cell:02x}'
            hex_line.append(cell)
        hex_line = ','.join(hex_line)
        hex_lines.append(hex_line)
    hex_content = '\n'.join(hex_lines)
    return hex_content

def main(args):
    input, output = args
    with open(input, 'r') as file:
        content = file.read()
    content = csv2hex(content)
    with open(output, 'w') as file:
        file.write(content)
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
