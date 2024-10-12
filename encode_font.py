
import sys

def decode_input(data):
    result_background = []
    result_foreground = []
    data = list(data)
    for i in range(0, 16):
        back = data[i*2]
        fore = data[i*2 + 1]
        result_background.append(back << 8)
        result_foreground.append(fore << 8)
    for i in range(0, 16):
        back = data[16*2 + i*2]
        fore = data[16*2 + i*2 + 1]
        result_background[i] |= back
        result_foreground[i] |= fore
    return result_background, result_foreground

def strip_char(data):
    data = data[2:]
    for i, row in enumerate(data):
        data[i] = row >> 6
    return data

def encode_char(background, foreground, compress=True):
    horizontal_strips = []
    vertical_strips = []

    for i in range(0, 14):
        background_strip = background[i] >> 2
        foreground_strip = foreground[i] >> 2
        horizontal_strips.append(background_strip)
        horizontal_strips.append(foreground_strip)

    def get_vertical_strip(start, end, shift):
        background_strip = 0
        foreground_strip = 0
        for i in range(start, end):
            background_strip <<= 1
            foreground_strip <<= 1
            background_strip |= (background[i] >> shift) & 1
            foreground_strip |= (foreground[i] >> shift) & 1
        return background_strip, foreground_strip

    def append_vertical_strip(strips):
        background_strip, foreground_strip = strips
        vertical_strips.append(background_strip)
        vertical_strips.append(foreground_strip)

    append_vertical_strip(get_vertical_strip(0, 6, 1))
    append_vertical_strip(get_vertical_strip(0, 6, 0))
    append_vertical_strip(get_vertical_strip(6, 14, 1))
    append_vertical_strip(get_vertical_strip(6, 14, 0))

    defs = []
    result_data = []
    for i in range(6):
        back, fore = horizontal_strips[i*2], horizontal_strips[i*2 + 1]
        def_value = 0
        if back != 0 or not compress:
            def_value |= 2
            result_data.append(back)
        if fore != 0 or not compress:
            def_value |= 1
            result_data.append(fore)
        defs.append(def_value)

    for i in range(2):
        back, fore = vertical_strips[i*2], vertical_strips[i*2 + 1]
        def_value = 0
        if back != 0 or not compress:
            def_value |= 2
            result_data.append(back)
        if fore != 0 or not compress:
            def_value |= 1
            result_data.append(fore)
        defs.append(def_value)

    defs.append(0)

    horizontal_strips = horizontal_strips[6*2:]
    vertical_strips = vertical_strips[2*2:]

    for i in range(8):
        back, fore = horizontal_strips[i*2], horizontal_strips[i*2 + 1]
        def_value = 0
        if back != 0 or not compress:
            def_value |= 2
            result_data.append(back)
        if fore != 0 or not compress:
            def_value |= 1
            result_data.append(fore)
        defs.append(def_value)

    for i in range(2):
        back, fore = vertical_strips[i*2], vertical_strips[i*2 + 1]
        def_value = 0
        if back != 0 or not compress:
            def_value |= 2
            result_data.append(back)
        if fore != 0 or not compress:
            def_value |= 1
            result_data.append(fore)
        defs.append(def_value)

    defs.append(0)

    result_def = []
    for i in range(5):
        d = 0
        for j in range(4):
            d <<= 2
            d |= defs[i*4 + j]
        result_def.append(d)

    return result_def, result_data

def main(args):
    input, out_def, out_table, out_data = args

    with open(input, 'rb') as f:
        input_data = f.read()
        input_data_len = len(input_data)

    out_def = open(out_def, 'wb')
    out_table = open(out_table, 'wb')
    out_data = open(out_data, 'wb')

    offset = 0
    char_len = 8 * 4 * 2 # bytes per tile * number of tiles * bits per pixel
    for i in range(0, input_data_len, char_len):
        background, foreground = decode_input(input_data[i:i+char_len])
        background, foreground = strip_char(background), strip_char(foreground)
        char_def, char_data = encode_char(background, foreground, True)
        out_def.write(bytearray(char_def))
        out_data.write(bytearray(char_data))
        out_table.write(bytearray([(offset & 0xff) >> 0, (offset & 0xff00) >> 8]))
        offset += len(char_data)

    count = input_data_len // char_len
    print(f'Encoded {count} characters.')
    out_def.close()
    out_table.close()
    out_data.close()

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
