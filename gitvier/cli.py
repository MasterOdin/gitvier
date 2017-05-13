#!/usr/bin/env python3

import argparse

from . import CLI, DESCRIPTION, VERSION, commands
from .logger import configure_logging


def _get_command(namespace):
    """

    :param args:
    :return:
    """
    args = []
    kwargs = {}

    def add_kwarg_force(kwargs, namespace):
        kwargs.update(force=namespace.force)

    def add_kwarg_clean(kwargs, namespace):
        kwargs.update(clean=namespace.clean)

    def add_kwarg_all(kwargs, namespace):
        add_kwarg_force(kwargs, namespace)
        add_kwarg_clean(kwargs, namespace)

    # because list is a good command name, but it is a reserved python keyword
    if namespace.command == 'list':
        namespace.command = 'display'

    command = getattr(commands, namespace.command, None)

    if namespace.command == 'init':
        add_kwarg_force(kwargs, namespace)

    """
        TODO: add these options
    if namespace.command in ('install', 'update'):
        add_kwarg_all(kwargs, namespace)
    """

    return command, args, kwargs


def main():
    force = argparse.ArgumentParser(add_help=False)
    force.add_argument('-f', '--force', action='store_true', default=False,
                       help="overwrite uncommitted changes in components")

    clean = argparse.ArgumentParser(add_help=False)
    clean.add_argument('-c', '--clean', action='store_true', default=False,
                       help="delete ignored files in components")

    options = argparse.ArgumentParser(add_help=False, parents=[force, clean])

    parser = argparse.ArgumentParser(prog=CLI, description=DESCRIPTION)
    parser.add_argument('-V', '--version', action="version", version=VERSION)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-v', '--verbose', dest="verbose", action='count', default=0)
    group.add_argument('-q', '--quiet', dest="verbose", action='store_const', const=-1)

    subparsers = parser.add_subparsers(dest='command', metavar='<command>')
    subparsers.add_parser('init', help='Initialize a new gitvier directory', parents=[force])

    subparsers.add_parser('install', help='', parents=[])

    subparsers.add_parser('update', help='', parents=[])

    subparsers.add_parser('list', help='')

    subparsers.add_parser('uninstall', help='', parents=[])

    namespace = parser.parse_args()
    if namespace.command is None:
        parser.print_help()
        raise SystemExit

    logger = configure_logging(namespace.verbose)
    logger.debug("Inputted command: {}".format(namespace.command))

    command, args, kwargs = _get_command(namespace)

    if command is None:
        parser.print_help()
        raise SystemExit

    try:
        command(*args, **kwargs)
    except KeyboardInterrupt:
        raise SystemExit("Command interrupted")

if __name__ == "__main__":
    main()
