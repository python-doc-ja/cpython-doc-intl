#!/usr/bin/env python3
import os
import path
import sys


def copy(lst, src, dst):
    with open(lst, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            print(line)
            src.joinpath(line).copy(dst.joinpath(line))


def main():
    lst, src, dst = sys.argv[1:]
    print("copying from {} to {}".format(src, dst))
    if input().lower()[0] != 'y':
        return
    copy(lst, path.Path(src), path.Path(dst))


if __name__ == '__main__':
    main()
