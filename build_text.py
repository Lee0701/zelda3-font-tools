
import sys
import yaml

def int2lst(num):
    if num == 0:
        return [0]
    result = []
    while num > 0:
        result.append(num & 0xFF)
        num >>= 8
    return result[::-1]

def main(args):
    tbl_file, input_file, output_file = args
    with open(tbl_file, 'r') as f:
        tbl_content = f.readlines()
    tbl_content = [line.replace('\n', '').replace('\r', '') for line in tbl_content]
    tbl_content = [line.split('=') for line in tbl_content]
    tbl_content = [entry for entry in tbl_content if len(entry) == 2]
    tbl_content = [(int(key, 16), value) for key, value in tbl_content]
    tbl_content = {value: key for key, value in tbl_content}
    max_key_len = max(len(key) for key in tbl_content.keys()) + 1

    content = ''

    with open(input_file, 'r') as f:
        content = yaml.load(f, yaml.SafeLoader)
    content = content.values()
    content = [line + '<end>' for line in content]
    content = ''.join(content)

    result = []

    offset = 0
    while offset < len(content):
        for k in reversed(range(1, max_key_len)):
            key = content[offset:offset+k]
            if key in tbl_content:
                value = tbl_content[key]
                value = int2lst(value)
                result += value
                offset += k
                break
        else:
            key = content[offset:offset+4]
            if key.startswith('<') and key.endswith('>'):
                value = int(key[1:-1], 16)
                result += int2lst(int(key[1:-1], 16))
                offset += 4
            else:
                print(f"Invalid key: {key}")
                return 1

    with open(output_file, 'wb') as f:
        f.write(bytearray(result))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
