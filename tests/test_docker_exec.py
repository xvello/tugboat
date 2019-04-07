import os
import hashlib

import docker
import pytest

from tugboat.docker import exec_in_container


@pytest.fixture(scope="module")
def container():
    """
    Spins up a dummy alpine container one can exec
    into and takes it down at the end of the test.
    """
    client = docker.from_env()
    container = client.containers.run(
        "alpine:3.9", "tail -f /dev/null", remove=True, detach=True
    )
    yield container

    container.stop()


def test_exec_ok_direct(container):
    assert exec_in_container(container.id, "ls /bin/busybox") == "/bin/busybox"


def test_exec_nok_direct(container):
    with pytest.raises(RuntimeError) as e:
        exec_in_container(container.id, "ls /does/not/exit")
        assert (
            str(e)
            == """
RuntimeError: Command ls /does/not/exit exited with 1:
ls: /does/not/exit: No such file or directory
        """
        )


def test_exec_nok_stream(container, tmp_path):
    f = str(tmp_path / "out")
    with pytest.raises(RuntimeError) as e:
        exec_in_container(container.id, "ls /does/not/exit", f)
        assert (
            str(e)
            == """
RuntimeError: Command ls /does/not/exit exited with 1:
ls: /does/not/exit: No such file or directory
        """
        )
    assert not os.path.exists(f)
    assert len(os.listdir(str(tmp_path))) == 0


def test_exec_ok_stream_text(container, tmp_path):
    f = str(tmp_path / "out")

    # Write dummy file to be replaced
    with open(f, "w") as file:
        file.write("fail")

    exec_in_container(container.id, 'echo -e "testing\ntesting"', f)

    # Check we only have one file (temp file removed)
    assert os.path.exists(f)
    assert len(os.listdir(str(tmp_path))) == 1

    # Check file contents
    with open(f, "r") as file:
        assert file.readline() == "testing\n"
        assert file.readline() == "testing\n"
        assert file.readline() == ""


def test_exec_ok_stream_binary(container, tmp_path):
    # Get file hash from the binary, trust busybox
    digest_output = exec_in_container(container.id, "sha256sum /bin/busybox")
    expected_digest = digest_output.split()[0]
    assert len(expected_digest) == 64

    f = str(tmp_path / "out")
    exec_in_container(container.id, "cat /bin/busybox", f)

    assert os.path.exists(f)
    assert len(os.listdir(str(tmp_path))) == 1

    sha256_hash = hashlib.sha256()
    with open(f, "rb") as file:
        # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
        file_digest = sha256_hash.hexdigest()

    assert file_digest == expected_digest
