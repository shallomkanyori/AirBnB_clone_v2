#!/usr/bin/python3
"""This module is a fabfile.

    Functions:
        deploy
"""
import os
from fabric.api import put, run, settings, env
do_pack = __import__('1-pack_web_static').do_pack
do_deploy = __import__('2-do_deploy_web_static').do_deploy

env.hosts = ['52.3.241.19', '54.237.48.59']


def deploy():
    """Creates and distributes an archive to some web servers.

    Returns:
        True if all operations have been done correctly.
        Otherwise, returns False.
    """

    archive_path = do_pack()

    if not archive_path:
        return False

    return do_deploy(archive_path)
