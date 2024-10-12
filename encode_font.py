
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

def encode_font(input_data, compress=True):
    result_def = []
    result_table = []
    result_data = []

    offset = 0
    char_len = 8 * 4 * 2 # bytes per tile * number of tiles * bits per pixel
    for i in range(0, len(input_data), char_len):
        char_data = input_data[i:i+char_len]
        background, foreground = decode_input(input_data[i:i+char_len])
        background, foreground = strip_char(background), strip_char(foreground)
        char_def, char_data = encode_char(background, foreground, compress)
        result_def += char_def
        result_table += [(offset & 0xff) >> 0, (offset & 0xff00) >> 8]
        result_data += char_data
        offset += len(char_data)

    return result_def, result_table, result_data

def main(args):
    input, out_def, out_table, out_data = args

    with open(input, 'rb') as f:
        input_data = f.read()
        input_data = list(input_data)

    result_def, result_table, result_data = encode_font(input_data, True)

    count = len(result_def) // 5
    print(f"Encoded {count} characters.")

    with open(out_def, 'wb') as f:
        f.write(bytearray(result_def))
    with open(out_table, 'wb') as f:
        f.write(bytearray(result_table))
    with open(out_data, 'wb') as f:
        f.write(bytearray(result_data))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
