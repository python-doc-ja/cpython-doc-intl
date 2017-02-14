#!/usr/bin/env python
from __future__ import print_function
import os
import re
import sys
import unicodedata

R0 = re.compile(r"""(?<![`\\])``.+?(?<![`\\])``""")
R1 = re.compile(r""":\w+:`.+?(?<=[^`\\])`""")
R2 = re.compile(r"""(?<![`\\])\*\*.*?[^ \\*]\*\*""")
R3 = re.compile(r"""(?<![`\\])\*.*?[^ \\*]\*""")
RX = re.compile(r"""(?<![`\\])``.+?(?<![`\\])``|:\w+:`.+?(?<=[^`\\])`|(?<![`\\])\*\*.*?[^ \\*]\*\*|(?<![`\\])\*.*?[^ \\*]\*""")

SPLITTER = """:,. ()[]'\"\r\n*/"""

#REX = [R0, R1, R2, R3]
REX = [RX]

def _test(uc, i):
    if not uc:
        return False
    uc = uc[i]
    return unicodedata.east_asian_width(uc) in ('W', 'F', 'A')

def char_filter(line):
    line = line.decode('utf-8')
    parts = line.split(' ')
    if not parts:
        return line
    parts_ = [parts[0]]
    i = 1
    while i < len(parts):
        if _test(parts[i-1], -1) and _test(parts[i], 0):
            parts_[-1] += parts[i]
        else:
            parts_.append(parts[i])
        i += 1
    return ' '.join(parts_).encode('utf-8')

def apply_line(line, n=0):
    line = line.rstrip() + line[-1]
    line = char_filter(line)
    if line.startswith('.. '):
        return line
    for r in REX:
        pos = 0
        buf = ""
        for m in r.finditer(line):
            print(n, m.group(0))
            start, end = m.span()
            buf += line[pos:start]
            if start > 0 and line[start-1] not in SPLITTER:
                buf += ' '
            buf += m.group(0)
            if line[end] not in SPLITTER:
                buf += ' '
            pos = end
        buf += line[pos:]
        line = buf
    return line

def test_to_lines(lines, out=sys.stdout):
    for l in lines:
        l_ = apply_line(l)
        if l_ != l:
            out.write('-')
            out.write(l)
            out.write('+')
            out.write(l_)

def apply_to_file(file):
    orig = file + '.orig'
    os.rename(file, orig)

    fi = open(orig, 'rb')
    fo = open(file, 'wb')

    for n, l in enumerate(fi):
        fo.write(apply_line(l, n))

    fi.close()
    fo.close()

def main():
    if len(sys.argv) > 1:
        for f in sys.argv[1:]:
            apply_to_file(f)
    else:
        for l in sys.stdin:
            sys.stdout.write(apply_line(l))

if __name__ == '__main__':
    main()
