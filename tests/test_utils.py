import pytest

from tugboat.utils import build_file_path, ensure_unique_filenames
from tugboat.docker import Job


def test_build_file_path_valid(tmp_path):
    p = build_file_path("test", str(tmp_path))
    assert p == str(tmp_path / "test")


def test_build_file_path_outside(tmp_path):
    with pytest.raises(ValueError):
        build_file_path("../test", str(tmp_path))


def test_build_file_path_empty():
    with pytest.raises(ValueError):
        build_file_path("", "/tmp")
    with pytest.raises(ValueError):
        build_file_path("test", "")


def test_ensure_unique_filenames_ok():
    jobs = [
        Job("", "one", "", "", "", "file1"),
        Job("", "two", "", "", "", "file2"),
        Job("", "three", "", "", "", "file3"),
    ]
    ensure_unique_filenames(jobs)

def test_ensure_unique_filenames_nok():
    jobs = [
        Job("", "one", "", "", "", "file1"),
        Job("", "two", "", "", "", "file2"),
        Job("", "three", "", "", "", "file1"),
    ]
    with pytest.raises(ValueError):
        ensure_unique_filenames(jobs)