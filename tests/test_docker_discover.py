import pytest

from tugboat.docker import discover_containers, Job

pytest_plugins = ["docker_compose"]


EXPECTED_JOBS = {
    "tests_all-annotations--yes_1": Job(
        "",
        "",
        "/my/pre/command",
        "/my/bkp/command with args",
        "/my/post/command",
        "redis-backup.gz",
    ),
    "tests_required-annotations--yes_1": Job(
        "", "", "", "/my/bkp/command with args", "", "redis-backup.gz"
    ),
}


def test_discover_containers(docker_containers):
    all_names = [c.name for c in docker_containers]
    expected_yes = [n for n in all_names if n.endswith("--yes_1")]
    expected_no = [n for n in all_names if n.endswith("--no_1")]
    assert set(all_names) == set(expected_yes + expected_no)

    # Wait for not-running--no to exit
    for c in docker_containers:
        if "not-running--no" not in c.name:
            continue
        c.wait()

    # Discover containers
    jobs = discover_containers()
    by_name = {}
    for j in jobs:
        by_name[j.name] = j

    # Test which containers have been detected
    for n in expected_yes:
        assert n in by_name
    for n in expected_no:
        assert n not in by_name

    # Test the parsing
    for name, job in EXPECTED_JOBS.items():
        assert by_name[name].bkp == job.bkp
        assert by_name[name].pre == job.pre
        assert by_name[name].post == job.post
        assert by_name[name].post == job.post
        assert by_name[name].filename == job.filename
