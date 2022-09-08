#!/usr/bin/env python3

def get_bad_chars(hexdump):
    hexdump.replace("\n", " ")
    hexdump.strip()
    chars = hexdump.split()
    start = chars.index("01")

    badchars = ["\\x00"]
    i = start
    while i < len(chars) - 1:
        char = chars[i]
        value = int(char, 16)
        if char == '00':
            i += 1
            continue

        char2 = chars[i + 1]
        value2 = int(char2, 16)
        if char2 == '00':
            i += 1
            continue

        s = value + value2
        if s % 2 == 0:  # Character is missing
            missing = "\\x" + format(int(s / 2), "02x")
            print(f"{missing} is missing. Likely a bad character.")
            badchars.append(missing)
        i += 1

    return badchars


def main():
    import sys

    dump_file = sys.argv[1]
    with open(dump_file, "r") as f:
        hexdump = f.read()

    badchars = get_bad_chars(hexdump)
    print(''.join(badchars))


if __name__ == '__main__':
    main()
