
import sys

text_len = 0x7356
text_start = 0x0e0000
text_end = text_start + text_len

def main(args):
    input_file, text_file, output_file = args

    with open(input_file, 'rb') as f:
        input_data = f.read()

    with open(text_file, 'rb') as f:
        text_data = f.read()

    if len(text_data) > text_len:
        print(f'Error: Text data is too long. ({len(text_data)} > {text_len} bytes)')
        return 1
    text_data = text_data + b'\xfb' * (text_len - len(text_data))

    output_data = input_data[:text_start] + text_data + input_data[text_end:]
    with open(output_file, 'wb') as f:
        f.write(output_data)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
