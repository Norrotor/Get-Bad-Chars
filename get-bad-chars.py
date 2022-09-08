#!/usr/bin/env python3

import sys

dump_file = sys.argv[1]
with open(dump_file, "r") as f:
    dump = f.read()

dump.replace("\n", " ")
dump.strip()
chars = dump.split()
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

print(''.join(badchars))
