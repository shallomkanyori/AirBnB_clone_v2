#!/usr/bin/python3
"""This module is a fabfile.

    Functions:
        do_pack
"""
from fabric.api import local
from datetime import datetime


def do_pack():
    """Generates a .tgz archive from ./web_static/ directory."""
    d = datetime.now()
    filepath = "versions/web_static_"
    filepath += f"{d.year}{d.month}{d.day}{d.hour}{d.minute}{d.second}.tgz"

    local("mkdir -p versions")
    cmd = f"tar -cvzf {filepath} web_static"

    res = local(cmd)

    if res.succeeded:
        return filepath
    else:
        return None
