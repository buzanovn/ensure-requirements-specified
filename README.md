# ensure-requirements-specified

## Description
Script checks whether all requirement files
has each requirement with version specified.\n\n

Requirements can be passed directly to script as positional arguments,
either it will traverse current working directory.
in search of a file with name that matches
`has 'requirements' in it and ends with '.txt'` condition.

## Usage
Can be used as a stadalone script or as an installable package
or as pre-commit hook

Standalone script:
  ```shell
  python3 ensure_requirements_specified.py --help
  ```

Installable package:

  Install via `python3 setup.py install` and then use with
  ```shell
  python3 -m ensure_requirements_specified --help
  ```
  or
  ```shell
  ensure-requirements-specified --help
  ```
Pre-commit hook:
  Add this to your .pre-commit-config.yaml
  ```yaml
  repos:
  ...
  -   repo: https://github.com/buzanovn/ensure-requirements-specified
      rev: v1.0.0
      hooks:
      -   id: ensure-requirements-specified
  ```
