import sys
import os
import requests
import time
import pathlib
import glob

base = sys.argv[1]
fp = open(sys.argv[2], "r")
codepoints = fp.readlines()
fp.close()

dir = []
for i in codepoints:
    i = i[:-1]
    c = i.split("-")[0]
    d1 = c[:-3]
    d2 = c[:-2]
    if not base + "/" + d1 + "/" + d2 in dir:
        dir.append(base + "/" + d1 + "/" + d2)
for i in dir:
    if not os.path.exists(i):
        os.makedirs(i)

temp = pathlib.Path(base)
svg = temp.glob("**/*.svg")
svg = map(lambda i: str(i), svg)
svg = set(svg)

for i in codepoints:
    i = i[:-1]
    c = i.split("-")[0]
    d1 = c[:-3]
    d2 = c[:-2]
    print("\r", i, sep="", end="        ")
    if not base + "/" + d1 + "/" + d2 + "/" + i + ".svg" in svg:
        if 0x1af90 <= int(c[1:], 16) <= 0x1afc2 or 0x1b123 <= int(c[1:], 16) <= 0x1b126 or 0x1b130 <= int(c[1:], 16) <= 0x1b131 or 0x1b133 <= int(c[1:], 16) <= 0x1b14f or 0x1b153 <= int(c[1:], 16) <= 0x1b154 or 0x1b156 <= int(c[1:], 16) <= 0x1b163 or c == "u1b168" or 0x2b73a <= int(c[1:], 16) <= 0x2b73f or 0x2cea2 <= int(c[1:], 16) <= 0x2cead or 0x323b0 <= int(c[1:], 16) <= 0x33479:
            url = "https://glyphwiki.org/glyph/unstable-" + i + ".svg"
        else:
            url = "https://glyphwiki.org/glyph/" + i + ".svg"
        count = 20
        while count > 0:
            data = requests.get(url).content
            if data[0:4] == b'<svg' and len(data) > 193:
                break
            print("\nfailed to get ... retry:", i, end='')
            time.sleep(1)
            count -= 1
        if data[0:4] == b'<svg' and len(data) > 193:
            with open(base + "/" + d1 + "/" + d2 + "/" + i + ".svg" ,mode='wb') as f:
                f.write(data)
        else:
            print("\nfailed to get:", i)

print("\r", end="")
