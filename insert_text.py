
import sys

table_start = 0x101000
text_start = 0x0e0000
text_len = 0x7356
text_end = text_start + text_len

def main(args):
    table_file, text_file, rom_file = args

    with open(rom_file, 'rb') as f:
        data = f.read()

    with open(table_file, 'rb') as f:
        table_data = f.read()

    with open(text_file, 'rb') as f:
        text_data = f.read()

    if len(text_data) > text_len:
        print(f'Error: Text data is too long. ({len(text_data)} > {text_len} bytes)')
        return 1
    text_data = text_data + b'\x00' * (text_len - len(text_data) - 1) + b'\xfb'

    # Patch the table
    table_len = len(table_data)
    table_end = table_start + table_len
    data = data[:table_start] + table_data + data[table_end:]

    # Patch the data
    data = data[:text_start] + text_data + data[text_end:]

    with open(rom_file, 'wb') as f:
        f.write(data)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
