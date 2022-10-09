from pathlib import Path

import pytest

from ensure_requirements_specified import process_file


def _get_data_file_path(name: str) -> str:
    return str(Path(__file__).parent / 'data' / name)


test_cases = [
    ('correct-one.txt', False),
    ('incorrect-one.txt', True),
]


@pytest.mark.parametrize('path, process_file_result', test_cases)
def test_file_returns_error_present(path: str, process_file_result: bool):
    path = _get_data_file_path(path)
    retv, _ = process_file(path)
    assert retv == process_file_result
