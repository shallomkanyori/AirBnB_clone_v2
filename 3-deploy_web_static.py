#!/usr/bin/python3
"""This module is a fabfile.

    Functions:
        do_pack
        do_deploy
        deploy
"""
import os
from fabric.api import *
from datetime import datetime

env.hosts = ['52.3.241.19', '54.237.48.59']
arch_path = None


@runs_once
def do_pack():
    """Generates a .tgz archive from ./web_static/ directory."""
    d = datetime.now()
    filepath = "versions/web_static_{}{}{}{}{}{}.tgz".format(d.year, d.month,
                                                             d.day, d.hour,
                                                             d.minute,
                                                             d.second)

    local("mkdir -p versions")
    cmd = f"tar -cvzf {filepath} web_static"

    res = local(cmd)

    if res.succeeded:
        return filepath
    else:
        return None


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


def deploy():
    """Creates and distributes an archive to some web servers.

    Returns:
        True if all operations have been done correctly.
        Otherwise, returns False.
    """

    arch_path = do_pack()

    if not arch_path:
        return False

    return do_deploy(arch_path)
