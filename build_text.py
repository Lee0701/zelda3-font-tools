
import sys
import yaml

end_token = '<end>'

def int2lst(num):
    if num == 0:
        return [0]
    result = []
    while num > 0:
        result.append(num & 0xFF)
        num >>= 8
    return result[::-1]

def main(args):
    tbl_file, base_text_file, text_file, output_table_file, output_data_file = args
    with open(tbl_file, 'r') as f:
        tbl_content = f.readlines()
    tbl_content = [line.replace('\n', '').replace('\r', '') for line in tbl_content]
    tbl_content = [line.split('=') for line in tbl_content]
    tbl_content = [entry for entry in tbl_content if len(entry) == 2]
    tbl_content = [(int(key, 16), value) for key, value in tbl_content]
    tbl_content = {value: key for key, value in tbl_content}
    max_key_len = max(len(key) for key in tbl_content.keys()) + 1

    with open(base_text_file, 'r') as f:
        base_content = yaml.load(f, yaml.SafeLoader)
        base_content = base_content.values()

    with open(text_file, 'r') as f:
        new_content = yaml.load(f, yaml.SafeLoader)
        new_content = new_content.values()

    end_token = '<end>'
    content = []
    for base, line in zip(base_content, new_content):
        if line == '':
            content.append(base)
        else:
            content.append(line)
    content = [line + end_token for line in content]
    content = ''.join(content)

    output_table = []
    output_data = []
    output_offset = 0x8000
    input_offset = 0

    output_table += [(output_offset & 0xff), ((output_offset >> 8) & 0xff)]

    while input_offset < len(content):
        for k in reversed(range(1, max_key_len)):
            key = content[input_offset:input_offset+k]
            if key in tbl_content:
                value = tbl_content[key]
                value = int2lst(value)
                output_data += value
                output_offset += len(value)
                input_offset += k
                if key == end_token:
                    output_table += [(output_offset & 0xff), ((output_offset >> 8) & 0xff)]
                break
        else:
            key = content[input_offset:input_offset+4]
            if key.startswith('<') and key.endswith('>'):
                value = int(key[1:-1], 16)
                output_data += int2lst(int(key[1:-1], 16))
                output_offset += 1
                input_offset += 4
            else:
                print(f"Invalid key: {key}")
                return 1

    with open(output_table_file, 'wb') as f:
        f.write(bytearray(output_table))

    with open(output_data_file, 'wb') as f:
        f.write(bytearray(output_data))

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
