from collections import namedtuple
import os

import docker

PRE_CMD_LABEL = "tugboat.pre_command"
BKP_CMD_LABEL = "tugboat.bkp_command"
POST_CMD_LABEL = "tugboat.post_command"
FILE_NAME_LABEL = "tugboat.filename"

Job = namedtuple("Job", ["cid", "name", "pre", "bkp", "post", "filename"])


def extract_label(c, name, default=""):
    """
    Return label value for a docker container
    """
    return c.labels.get(name, default)


def discover_containers():
    """
    List all running docker containers, then return the ones
    with the relevant tugboat labels, as a list of Job
    named tuples.
    """
    client = docker.from_env()
    found = []

    for c in client.containers.list():
        if BKP_CMD_LABEL not in c.labels or FILE_NAME_LABEL not in c.labels:
            continue
        found.append(
            Job(
                c.id,
                c.name,
                extract_label(c, PRE_CMD_LABEL),
                extract_label(c, BKP_CMD_LABEL),
                extract_label(c, POST_CMD_LABEL),
                extract_label(c, FILE_NAME_LABEL),
            )
        )

    return found


def exec_in_container(cid, cmd, stdout_path=None):
    client = docker.from_env()

    stream = False
    if stdout_path:
        stream = True

    resp = client.api.exec_create(cid, cmd, stdout=True, stderr=True)
    exec_output = client.api.exec_start(resp["Id"], stream=stream, demux=stream)

    if stdout_path:
        output = ""
        tmp_path = stdout_path + ".new"
        with open(tmp_path, "wb") as f:
            for chunk in exec_output:
                if chunk and chunk[0] is not None:
                    f.write(chunk[0])
                if chunk and chunk[1] is not None:
                    output += chunk[1].decode("utf-8")
    else:
        output = exec_output.decode("utf-8")

    exit_code = client.api.exec_inspect(resp["Id"])["ExitCode"]
    if exit_code:
        if stdout_path:
            os.remove(tmp_path)
        raise RuntimeError(
            "Command {} exited with {}:\n{}".format(cmd, exit_code, output)
        )

    if stdout_path:
        os.replace(tmp_path, stdout_path)
    else:
        return output.strip()
