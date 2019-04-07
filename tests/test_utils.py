import pytest

from tugboat.utils import build_file_path


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
