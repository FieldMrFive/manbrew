import os
import sys
import shutil
from core import TextStyle

__all__ = [
    'link_command',
    'unlink_command',
    'remove_command',
    'list_command',
    'root_command'
]


def container_exist(**kwargs):
    app_args, logger, manbrew_root = kwargs['app_args'], kwargs['logger'], kwargs['manbrew_root']
    container_path = os.path.join(manbrew_root, "Containers", app_args.container)
    if not os.path.exists(container_path):
        logger.warning("%s does not exist.", TextStyle.bold(app_args.container))
        return False
    return True


def link_command(**kwargs):
    if not container_exist(**kwargs):
        return

    app_args, manager, logger, manbrew_root = (
        kwargs['app_args'], kwargs['manager'], kwargs['logger'], kwargs['manbrew_root'])

    src_path = os.path.join(manbrew_root, "Containers", app_args.container)
    manager.link(container=app_args.container, src_path=src_path, dst_path=app_args.dst)


def unlink_command(**kwargs):
    if not container_exist(**kwargs):
        return

    app_args, manager = kwargs['app_args'], kwargs['manager']
    manager.unlink(container=app_args.container)


def remove_command(**kwargs):
    if not container_exist(**kwargs):
        return

    app_args, manager, logger, manbrew_root = (
        kwargs['app_args'], kwargs['manager'], kwargs['logger'], kwargs['manbrew_root'])

    if manager.container_linked(app_args.container):
        manager.unlink(container=app_args.container)

    rm_dir = os.path.join(manbrew_root, "Containers", app_args.container)
    if os.path.exists(rm_dir):
        logger.info("remove dir: %s", rm_dir)
        shutil.rmtree(rm_dir)
        logger.info("%s removed.", TextStyle.bold(app_args.container))


def list_command(**kwargs):
    manager, logger, manbrew_root = kwargs['manager'], kwargs['logger'], kwargs['manbrew_root']
    container_dir = os.path.join(manbrew_root, "Containers")
    message = "List All Containers\n"
    containers = []
    for container in os.listdir(container_dir):
        if not os.path.isdir(os.path.join(container_dir, container)):
            continue
        message += "%s" + (": linked\n" if manager.container_linked(container) else ": not linked\n")
        containers.append(TextStyle.bold(container))
    logger.info(message, *containers)


def root_command(**kwargs):
    sys.stdout.write(kwargs['manbrew_root'])
