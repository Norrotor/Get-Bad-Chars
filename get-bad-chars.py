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
        char2 = chars[i + 1]
        char_int = int(char, 16)
        char_int2 = int(char2, 16)
        
        if char2 == '00':
            missing = format(char_int + 1, "02x")
            chars[i + 1] = missing  # Update null byte in hexdump
            badchar = "\\x" + missing
            if verbose:
                print(f"{badchar} was null. Probably a bad character.")
            badchars.append(badchar)
            i += 1
            continue

        s = char_int + char_int2
        if s % 2 == 0:  # Character is missing
            missing = "\\x" + format(int(s / 2), "02x")
            if verbose:
                print(f"{missing} is missing. Probably a bad character.")
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

