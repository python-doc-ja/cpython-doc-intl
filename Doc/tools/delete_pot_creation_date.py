# -*- coding: utf-8 -*-

import io
import os
import sys


def delete_pot_creation_date(filename):
    with io.open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    with io.open(filename, 'w', encoding='utf-8') as f:
        f.writelines((line for line in lines if not line.startswith('"POT-Creation-Date: 20')))


def main(basedir):
    for dirpath, _, filenames in os.walk(basedir):
        for filename in filenames:
            if filename.endswith('.pot'):
                delete_pot_creation_date(os.path.join(dirpath, filename))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('too few argument')
        print('Usage: {0} <basedir>'.format(sys.argv[0]))
        sys.exit(1)
    sys.exit(main(sys.argv[1]))
