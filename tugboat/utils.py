import os


def build_file_path(filename, root_path):
    if not filename:
        raise ValueError("empty filename")
    if not root_path:
        raise ValueError("empty root path")

    abs_root = os.path.abspath(root_path)

    path = os.path.join(abs_root, filename)
    realpath = os.path.realpath(path)

    if not realpath.startswith(abs_root):
        raise ValueError(
            "file {} is outside of the specified folder {}".format(realpath, root_path)
        )
    return realpath


def ensure_unique_filenames(jobs):
    found = {}
    for j in jobs:
        if j.filename in found:
            raise ValueError("Duplicate filename {} for {} and {}".format(j.filename, j.name, found[j.filename].name))
        else:
            found[j.filename] = j
