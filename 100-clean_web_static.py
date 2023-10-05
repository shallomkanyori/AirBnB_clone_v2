#!/usr/bin/python3
"""This module contains a function that deletes out-od-date archives."""
from fabric.api import *

env.hosts = ['52.3.241.19', '54.237.48.59']


@runs_once
def clean_local(number):
    """Deletes out-of-date archives locally.

    Args:
        number (int): the number of archives to keep
    """

    arcs = local("ls -t versions/web_static_*", capture=True).split()

    for i in range(number, len(arcs)):
        local(f"rm {arcs[i]}")


def clean_remote(number):
    """Deletes out-of-date archives on remote hosts.

    Args:
        number (int): the number of archives to keep
    """

    arcs = run("ls -dt /data/web_static/releases/web_static_*").split()

    for i in range(number, len(arcs)):
        run(f"rm -r {arcs[i]}")


def do_clean(number=0):
    """Deletes out-of-date archives.

    Args:
        number (int): the number of archives to keep
    """

    number = int(number)
    number = 1 if number <= 0 else number

    clean_local(number)
    clean_remote(number)
