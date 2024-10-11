
import sys

def main(args):
    tbl_file, input_file, output_file = args
    with open(tbl_file, 'r') as f:
        tbl_content = f.readlines()
    tbl_content = [line.replace('\n', '').replace('\r', '') for line in tbl_content]
    tbl_content = [line.split('=') for line in tbl_content]
    tbl_content = [entry for entry in tbl_content if len(entry) == 2]
    tbl_content = [(key.lower(), value) for key, value in tbl_content]
    tbl_content = {key: value for key, value in tbl_content}

    with open(input_file, 'rb') as f:
        content = f.read()

    result = []

    offset = 0
    while offset < len(content):
        for k in reversed(range(1, 6)):
            key = content[offset:offset+k]
            key = ''.join(f'{k:02x}' for k in key).lower()
            if key in tbl_content:
                value = tbl_content[key]
                value = offset + 1, value
                result.append(value)
                offset += k
                break
        else:
            value = f'<{key}>'
            value = offset + 1, value
            result.append(value)
            offset += 1

    with open(output_file, 'w') as f:
        f.write(f'{0:06x}\t')
        for offset, token in enumerate(result):
            offset, token = token
            f.write(token)
            if token == '<end>':
                f.write('\n')
                if offset < len(content) - 1:
                    f.write(f'{offset:06x}\t')

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
