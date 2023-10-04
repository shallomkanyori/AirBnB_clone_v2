#!/usr/bin/python3
"""This module is a fabfile.

    Functions:
        do_deploy
"""
import os
from fabric.api import put, run, settings, env

env.hosts = ['52.3.241.19', '54.237.48.59']


def do_deploy(archive_path):
    """Distributes an archive to some web servers.

    Args:
        archive_path (str): the path to the archive.

    Returns:
        True if all operations have been done correctly.
        Otherwise, returns False.
    """

    if not os.path.exists(archive_path):
        return False

    with settings(abort_exception=Exception):
        try:
            fext = archive_path[archive_path.rfind('/') + 1:]
            fname = fext[:fext.rfind('.')]
            rem_path = f"/data/web_static/releases/{fname}"

            put(archive_path, "/tmp")

            run(f"mkdir -p  {rem_path}")
            run(f"tar -xzf /tmp/{fext} -C {rem_path}")

            run(f"rm /tmp/{fext}")

            run(f"mv {rem_path}/web_static/* {rem_path}")
            run(f"rm -rf {rem_path}/web_static")

            run("rm -rf /data/web_static/current")
            run(f"ln -s {rem_path} /data/web_static/current")

        except Exception:
            return False

    return True
