#!/usr/bin/python3
"""
Script checks whether all requirement files
has each requirement with version specified.\n\n

Requirements can be passed directly to script as positional arguments,
either it will traverse current working directory.
in search of a file with name that matches
`has 'requirements' in it and ends with '.txt'` condition.
"""

__usage__ = """
Can be used as a stadalone script or as an installable package
or as pre-commit hook

Standalone script:
  python3 ensure_requirements_specified.py --help

Installable package:
  Install via `python3 setup.py install` and then use with
  python3 -m ensure_requirements_specified --help

Pre-commit hook:
  Add this to your .pre-commit-config.yaml
    -   repo: https://github.com/buzanovn/ensure-requirements-specified
    rev: v1.1.0
    hooks:
    -   id: ensure-requirements-specified
"""

import argparse
import os
import re
from typing import Iterator
from typing import List
from typing import Optional
from typing import Sequence
from typing import Tuple
from typing import Union

from pip._internal.req import InstallRequirement
from pip._internal.req import parse_requirements
from pip._internal.req.constructors import install_req_from_parsed_requirement
from pip._internal.req.req_file import ParsedRequirement

REQUIREMENTS_REGEX = r'''^.*requirements.*.txt$'''


def parse_requirements_file(path: str) -> Iterator[InstallRequirement]:
    pr: ParsedRequirement
    for pr in parse_requirements(path, session=None):  # type: ignore
        yield install_req_from_parsed_requirement(pr)


def filter_no_specifier(
    it: Iterator[InstallRequirement],
) -> Iterator[InstallRequirement]:
    for install_requirement in it:
        if len(install_requirement.specifier) == 0:
            yield install_requirement


def process_file(path: str) -> Tuple[bool, List[str]]:
    errors = []
    found_packages_without_specifier = False
    for ir in filter_no_specifier(parse_requirements_file(path)):
        errors.append(
            f'{path}: No version specifier for package "{str(ir.req)}"',
        )
        found_packages_without_specifier = True
    return found_packages_without_specifier, errors


def process_many_files(
    paths: Iterator[str],
    verbose: bool = False,
) -> Tuple[bool, List[str]]:
    retv, errors = False, []
    for filename in paths:
        if verbose:
            print(f'Processing requirements file: {filename}')
        retv_file, errors_file = process_file(filename)
        retv |= retv_file
        errors.extend(errors_file)
    return retv, errors


def check_path_is_requirements_file(path: str) -> bool:
    path = os.path.basename(path)
    return re.match(REQUIREMENTS_REGEX, path) is not None


def iterate_files(
    root_dir: Optional[str] = None,
) -> Iterator[str]:
    if root_dir is None:
        root_dir = os.getcwd()

    for root, _, files in os.walk(root_dir):
        yield from (os.path.join(root, f) for f in files)


def main(argv: Union[Sequence[str], None] = None) -> int:
    parser = argparse.ArgumentParser(usage=__usage__, description=__doc__)
    parser.add_argument(
        'filenames', nargs='*',
        help='Paths to requirements files to check',
    )
    parser.add_argument(
        '--only-warn', '-w', action='store_true',
        help='Script will exit with status code 0 even if there are errors',
    )
    parser.add_argument(
        '--verbose', '-v', action='store_true',
        help='Script will output all requirement files processed',
    )
    parser.add_argument(
        '--skip-check-filenames', '-s', action='store_true',
        help='Supress filename check (check any file given)',
    )
    args = parser.parse_args(argv)

    file_path_iterator: Iterator[str]
    if len(args.filenames) == 0:
        file_path_iterator = iterate_files()
    else:
        file_path_iterator = iter(args.filenames)

    if args.skip_check_filenames:
        def file_name_filter_fn(x: str) -> bool:
            return True
    else:
        def file_name_filter_fn(x: str) -> bool:
            return check_path_is_requirements_file(x)

    file_path_iterator = filter(file_name_filter_fn, file_path_iterator)

    retv, errors = process_many_files(file_path_iterator, args.verbose)
    for err in errors:
        print(err)

    return 0 if args.only_warn else retv


__all__ = ['process_file']

if __name__ == '__main__':
    raise SystemExit(main())
