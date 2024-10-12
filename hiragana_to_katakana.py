
import sys

hiragana = 0x3040
katakana = 0x30a0
kana_len = 0x60
kana_diff = katakana - hiragana

def main(args):
    input, output = args

    with open(input, 'r') as f:
        content = f.read()

    result = ''

    for c in content:
        c = ord(c)
        if c in range(hiragana, hiragana + kana_len + 1):
            c += kana_diff
        result += chr(c)

    with open(output, 'w') as f:
        f.write(result)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
