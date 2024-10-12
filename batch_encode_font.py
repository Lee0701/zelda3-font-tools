
import sys
from encode_font import encode_font

def main(args):
    input, output = args

    with open(input, 'rb') as f:
        input_data = f.read()

    segment_len = 0x8000
    result_len = len(input_data) // segment_len


    bank_size = 0x8000
    result = []

    for i in range(result_len):
        segment = input_data[i * segment_len : (i + 1) * segment_len]
        result_def, result_table, result_data = encode_font(segment, False)
        if i == 0:
            result += result_def
            result += result_table
            result += [0] * (bank_size - len(result))
        result_data += [0] * (bank_size - len(result_data))
        result += result_data

    with open(output, 'wb') as f:
        f.write(bytearray(result))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
