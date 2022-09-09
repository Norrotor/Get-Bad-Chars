#!/usr/bin/env python3

def get_bad_chars(hexdump: str, verbose: bool = False):
    """Get bad characters from hexdump. Returns list of bad characters. Null ('00') characters and characters not in
    the dump are considered bad.

    :param hexdump: hexdump. Can include newlines.
    :param verbose: If set, print bad characters as they are found.
    :return: list of bad characters. Characters are in format "\xFF"
    """

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

        if char2 == '00':  # Next byte is null, give it the correct value according to the current byte
            null_value = format(char_int + 1, "02x")
            chars[i + 1] = null_value  # Update null byte in hexdump
            missing = "\\x" + null_value
            if verbose:
                print(f"{missing} was null. Probably a bad character.")
            badchars.append(missing)
        else:  # Next byte is not null
            for j in range(char_int + 1, char_int2):  # Check for missing bytes
                missing = "\\x" + format(int(j), "02x")
                if verbose:
                    print(f"{missing} is missing. Probably a bad character.")
                badchars.append(missing)

        i += 1

    return badchars


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Get bad characters from hexdump. Null ('00') characters and "
                                                 "characters not in the dump are considered bad.")
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

