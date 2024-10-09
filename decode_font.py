
#
# Decodes font data from ALttP JP
#

# 폰트 데이터 型式에 關하여
#
# 重要한 데이터 位置는 다음과 같다.
## 0x73840: 폰트 데이터 定義
## 0x70000: 實際 폰트 데이터
#
# 폰트 데이터 定義는 各 글字마다 5바이트씩 構成된다.
# 5바이트 데이터는 各各 2비트씩 나누어진다.
# 各 2비트는 該當 글字의 한 行을 意味하는데,
## 앞 비트는 그 行에 外郭線 픽셀이 存在하는지,
## 뒤 비트는 그 行에 內部 픽셀이 存在하는지
# 를 나타낸다.

# 實際 폰트 데이터에는 各 글字마다 該當하는 定義 데이터에 있는
# 1의 個數만큼의 바이트 數가 온다.
# 이 바이트들은 픽셀이 存在한다고 標示된 行들의 實際 픽셀 데이터이다.

# 한 글字의 크기는 10*14이므로 한 바이트로 1行을 모두 表現할 수 없다.
# 따라서, 오른쪽 두 列은 各各 上下로 나눠,
# 4바이트로 세로로 세워 나타낸다.
# 폰트 데이터 定義에서 2비트씩 分割한 總 20個 데이터의 패턴은 다음과 같다.

# 1 1 1 1 1 1 2 2 . 3 3 3 3 3 3 3 3 4 4 .

# 이 패턴은 實際로 다음과 같이 配置된다.

# . . . . . . . . 2 2
# . . . . . . . . 2 2
# 1 1 1 1 1 1 1 1 2 2
# 1 1 1 1 1 1 1 1 2 2
# 1 1 1 1 1 1 1 1 2 2
# 1 1 1 1 1 1 1 1 2 2
# 1 1 1 1 1 1 1 1 2 2
# 1 1 1 1 1 1 1 1 2 2
# 3 3 3 3 3 3 3 3 4 4
# 3 3 3 3 3 3 3 3 4 4
# 3 3 3 3 3 3 3 3 4 4
# 3 3 3 3 3 3 3 3 4 4
# 3 3 3 3 3 3 3 3 4 4
# 3 3 3 3 3 3 3 3 4 4
# 3 3 3 3 3 3 3 3 4 4
# 3 3 3 3 3 3 3 3 4 4

# 10*14를 上下 2分割하기 때문에 세로로 된 第2類 데이터는 2픽셀 위로 超過하여 配置된다.

import sys

def decode_char_def(char_def):
    result = []
    for d in char_def:
        d0 = (d & 0xc0) >> 6
        d1 = (d & 0x30) >> 4
        d2 = (d & 0x0c) >> 2
        d3 = (d & 0x03) >> 0
        result += [d0, d1, d2, d3]
    return result

def get_char_data_len(char_def):
    bit_count = [((d & 2) >> 1) + (d & 1) for d in char_def]
    return sum(bit_count)

def decode_char(char_def, char_data):
    # Pad top two rows
    result_background = [0, 0]
    result_foreground = [0, 0]

    columns_background = []
    columns_foreground = []

    char_data = list(char_data)

    horizontal_indices = set([0, 1, 2, 3, 4, 5, 9, 10, 11, 12, 13, 14, 15, 16])
    vertical_indices = set([6, 7, 17, 18])

    for i, d in enumerate(char_def):
        if i in horizontal_indices:
            row = char_data.pop(0) if d & 2 else 0
            result_background.append(row)
            row = char_data.pop(0) if d & 1 else 0
            result_foreground.append(row)
        elif i in vertical_indices:
            column = char_data.pop(0) if d & 2 else 0
            columns_background.append(column)
            column = char_data.pop(0) if d & 1 else 0
            columns_foreground.append(column)

    # Appends a column to each row, starting from the offset.
    def append_column(rows, column, offset=0):
        for i in range(offset, offset+8):
            bit = (column & 0x80) >> 7
            column <<= 1
            rows[i] <<= 1
            rows[i] |= bit
        return rows

    for o in [0, 0, 8, 8]:
        column_background = columns_background.pop(0)
        append_column(result_background, column_background, o)
        column_foreground = columns_foreground.pop(0)
        append_column(result_foreground, column_foreground, o)

    # Remove padding rows
    result_background = result_background[2:]
    result_foreground = result_foreground[2:]

    return result_background, result_foreground

def main(args):
    font_def, font_data, output = args
    with open(font_def, 'rb') as f:
        font_def = f.read()
    with open(font_data, 'rb') as f:
        font_data = f.read()
    output = open(output, 'w')

    char_count = len(font_def) // 5
    for i in range(char_count):
        char_def = decode_char_def(font_def[i*5:i*5+5])
        data_len = get_char_data_len(char_def)
        background, foreground = decode_char(char_def, font_data)
        for line in background:
            output.write(f'{line:010b}'.replace('0', '.'))
            output.write('\n')
        output.write('\n')
        for line in foreground:
            output.write(f'{line:010b}'.replace('0', '.'))
            output.write('\n')
        output.write('\n')
        font_data = font_data[data_len:]
    print(f'Decoded {char_count} characters.')
    output.close()
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
