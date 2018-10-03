from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals

import subprocess
import glob
import re
from collections import defaultdict


GIVEN_PAT = re.compile('^Given\(\"(.+)\", .+$')
WHEN_PAT = re.compile('^When\(\"(.+)\", .+$')
THEN_PAT = re.compile('^Then\(\"(.+)\", .+$')


def main(argv=None):
    givens = defaultdict(list)
    whens = defaultdict(list)
    thens = defaultdict(list)

    for filename in glob.iglob('**/stepdefinitions/**/*.ts', recursive=True):
        with open(filename) as f:
            for line in f.readlines():
                m = GIVEN_PAT.match(line)
                if m:
                    givens[filename].append(m.groups()[0])

                m = WHEN_PAT.match(line)
                if m:
                    whens[filename].append(m.groups()[0])

                m = THEN_PAT.match(line)
                if m:
                    thens[filename].append(m.groups()[0])

    _write_to_file('compiled_given_steps.txt', givens)
    _write_to_file('compiled_when_steps.txt', whens)
    _write_to_file('compiled_then_steps.txt', thens)

    subprocess.call('git add compiled_given_steps.txt'.split(), stdout=subprocess.PIPE)
    subprocess.call('git add compiled_when_steps.txt'.split(), stdout=subprocess.PIPE)
    subprocess.call('git add compiled_then_steps.txt'.split(), stdout=subprocess.PIPE)
    return 0


def _write_to_file(fname, steps):
    with open(fname, 'w') as f:
        first = True
        for k, vv in sorted(steps.items(), key=lambda x: x[0]):
            if first:
                first = False
            else:
                f.write('\n')
            idx = k.find('stepdefinitions')
            f.write(k[idx + 16:])
            f.write('\n')
            for v in sorted(vv):
                f.write('\t')
                f.write(v)
                f.write('\n')


if __name__ == '__main__':
    exit(main())
