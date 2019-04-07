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
