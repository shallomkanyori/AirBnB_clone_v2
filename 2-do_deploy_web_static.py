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

    fext = archive_path[archive_path.rfind('/') + 1:]
    fname = fext[:fext.rfind('.')]
    rem_path = f"/data/web_static/releases/{fname}"

    # upload file
    if put(archive_path, "/tmp").failed:
        return False

    # unpack files
    if run(f"mkdir -p  {rem_path}").failed:
        return False

    if run(f"tar -xzf /tmp/{fext} -C {rem_path}").failed:
        return False

    # remove extra directories
    if run(f"rm /tmp/{fext}").failed:
        return False

    if run(f"mv {rem_path}/web_static/* {rem_path}").failed:
        return False

    if run(f"rm -rf {rem_path}/web_static").failed:
        return False

    # update symlink
    if run("rm -rf /data/web_static/current").failed:
        return False

    if run(f"ln -s {rem_path} /data/web_static/current").failed:
        return False

    return True
