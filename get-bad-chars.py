#!/usr/bin/env python3

def get_bad_chars(hexdump: str, verbose: bool = False):
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
            if verbose:
                print(f"{missing} is missing. Likely a bad character.")
            badchars.append(missing)
        i += 1

    return badchars


def main():
    import argparse

    parser = argparse.ArgumentParser(description='Get bad characters from hexdump. '
                                                 'At the moment, only missing characters are considered bad.')
    parser.add_argument("file", help="File containing hexdump")
    parser.add_argument("-v", "--verbose", help="Increase verbosity", action="store_true")

    args = parser.parse_args()

    dump_file = args.file
    with open(dump_file, "r") as f:
        hexdump = f.read()

    badchars = get_bad_chars(hexdump, args.verbose)
    print(''.join(badchars))


if __name__ == '__main__':
    main()

