#!/usr/bin/python3
"""This module is a fabfile that distributes an archive to web servers.
"""
import os
from fabric.api import put, run, env

env.hosts = ['52.3.241.19', '54.237.48.59']


def do_deploy(archive_path):
    """Distributes an archive to some web servers.

    Args:
        archive_path (str): the path to the archive.

    Returns:
        True if all operations have been done correctly.
        Otherwise, returns False.
    """

    if not os.path.isfile(archive_path):
        return False

    f = archive_path.split('/')[-1]
    fname = f.split('.')[0]
    path = "/data/web_static/releases/{}/".format(fname)

    try:
        # upload file
        put(archive_path, "/tmp/{}".format(f))

        # unpack files
        run("mkdir -p {}".format(path))
        run("tar -xzf /tmp/{} -C {}".format(f, path))

        # remove extra directories
        run("rm /tmp/{}".format(f))

        run("mv {}web_static/* {}".format(path, path))

        run("rm -rf {}web_static".format(path))

        # update symlink
        run("rm -rf /data/web_static/current")
        run("ln -s {} /data/web_static/current".format(path))
        print("New version deployed!")
        return True
    except Exception:
        return False
